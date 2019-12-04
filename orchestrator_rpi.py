import time
import uuid

from orchestrator_status import OrchestratorStatus
# from industrial_informatic_assigment.workstation.pallet import Pallet
# from industrial_informatic_assigment.workstation.phone import Phone
from workstation import Workstation, Phone, Pallet
from enum_variables import StatusCode, Zone, PalletStatus


class Orchestrator:

    def __init__(self, orchestratorStatus: OrchestratorStatus, workstation: Workstation):
        self.orchestratorID = uuid.uuid4()
        self.ws = workstation
        self.bufferOrder = []
        self.status = orchestratorStatus
        print("Initialization: new orchestrator  (" + str(self.orchestratorID) + ")")

    def runOrchestration(self):
        while True:
            self.testZone1()
            self.testZone2()
            self.testZone3()
            self.testZone4()
            self.printPalletInfo()
            time.sleep(4)

    def addOrder(self, phone: Phone):
        print("Orchestrator object: new phone added to order list")
        if self.ws.conveyor.getZoneStatus(Zone.Z1) == -1:
            print("Orchestrator object: add to buffer 1")
            self.addOrderToBuffer(phone)
        elif self.testIfZoneFree(Zone.Z1):
            print("Orchestrator object: add to buffer 1")
            self.addOrderToBuffer(phone)
        else:
            print("Orchestrator object: add to pallet")
            palletId = self.ws.conveyor.getZoneStatus(Zone.Z1)
            self.addPhoneToPallet(palletId, phone)

    def addOrderToBuffer(self, phone: Phone):
        if len(self.bufferOrder) >= 2:
            print("Orchestrator object: max number of orders are already reached")
            return
        self.bufferOrder.append(phone)

    def penSelectEndEvent(self):
        pallet = self.getPalletFromZone(Zone.Z2)
        pallet.status = PalletStatus.WAITING

    def penSelectStartEvent(self):
        pass

    def testIfZoneFree(self, zone: Zone) -> bool:
        if len(self.ws.pallets) > 0:
            for pallet in self.ws.pallets:
                if pallet.locationZone == zone:
                    return True
        return False

    def addPhoneToPallet(self, id, phone: Phone):
        pallet = Pallet(id, phone, self.ws, Zone.Z1)
        pallet.status = PalletStatus.WAITING
        self.addPalletToWS(pallet)

    def addPalletToWS(self, pallet):
        if len(self.ws.pallets) >= 5:
            print("Orchestrator object: there are already 5 pallets in the ws")
        self.ws.pallets.append(pallet)

    def drawEndEvent(self):
        pallet = self.getPalletWithStatus(PalletStatus.DRAWING)
        if not pallet.frameDone or not pallet.screenDone or not pallet.keyboardDone:
            pallet.status = PalletStatus.WAITING
            return
        pallet.status = PalletStatus.WAITING

    def testIfPalletWithStatusExist(self, status: PalletStatus) -> bool:
        for pallet in self.ws.pallets:
            if pallet.status == status:
                return True
        return False

    def getPalletFromZone(self, zone: Zone) -> Pallet:
        for pallet in self.ws.pallets:
            if pallet.locationZone == zone:
                return pallet
        print("Orchestrator object: couldn't find pallet on zone: " + str(zone.name))

    def getPalletWithStatus(self, status: PalletStatus):
        for pallet in self.ws.pallets:
            if pallet.status == status:
                return pallet
        print("Orchestrator object: couldn't find pallet with that status: " + str(status.name))

    def drawStartEvent(self):
        pass

    def testZone1(self):
        if not self.testIfZoneFree(Zone.Z1):
            return
        pallet = self.getPalletFromZone(Zone.Z1)
        if pallet.status == PalletStatus.MOVING_TO_Z2:
            return
        if not self.testIfZoneFree(Zone.Z2) and not self.testIfPalletWithStatusExist(PalletStatus.MOVING_TO_Z2):
            print("Orchestrator object: move pallet from zone 1 to zone 2")
            pallet.status = PalletStatus.MOVING_TO_Z2
            self.ws.conveyor.movePallet(Zone.Z1, Zone.Z2)
            return
        if not self.testIfZoneFree(Zone.Z4) and not self.testIfPalletWithStatusExist(PalletStatus.MOVING_TO_Z4):
            print("Orchestrator object: move pallet from zone 1 to zone 4")
            pallet.status = PalletStatus.MOVING_TO_Z4
            self.ws.conveyor.movePallet(Zone.Z1, Zone.Z4)

    def testZone2(self):
        if not self.testIfZoneFree(Zone.Z2):
            return
        pallet = self.getPalletFromZone(Zone.Z2)
        if pallet.status == PalletStatus.MOVING_TO_Z3:
            return
        elif pallet.status == PalletStatus.WAITING and not self.testIfZoneFree(Zone.Z3):
            print("Orchestrator object: move pallet from zone 2 to zone 3")
            self.ws.conveyor.movePallet(Zone.Z2, Zone.Z3)
            pallet.status = PalletStatus.MOVING_TO_Z3


    def testZone3(self):
        if not self.testIfZoneFree(Zone.Z3):
            return
        pallet = self.getPalletFromZone(Zone.Z3)
        if pallet.status == PalletStatus.MOVING_TO_Z4 or pallet.status == PalletStatus.DRAWING:
            return
        if pallet.status == PalletStatus.WAITING:
            if not pallet.frameDone:
                pallet.status = PalletStatus.DRAWING
                self.ws.robot.executeDrawing(pallet.phone.frameShape)
                pallet.frameDone = True
            elif not pallet.screenDone:
                pallet.status = PalletStatus.DRAWING
                self.ws.robot.executeDrawing(pallet.phone.screenShape)
                pallet.screenDone = True
            elif not pallet.keyboardDone:
                pallet.status = PalletStatus.DRAWING
                self.ws.robot.executeDrawing(pallet.phone.keyboardShape)
                pallet.keyboardDone = True
            elif not self.testIfZoneFree(Zone.Z5) and not self.testIfPalletWithStatusExist(PalletStatus.MOVING_TO_Z5):
                print("Orchestrator object: move pallet from zone 3 to zone 5")
                pallet.status = PalletStatus.MOVING_TO_Z5
                self.ws.conveyor.movePallet(Zone.Z3, Zone.Z5)

    def testZone4(self):
        if not self.testIfZoneFree(Zone.Z4):
            return
        pallet = self.getPalletFromZone(Zone.Z4)
        if pallet.status == PalletStatus.MOVING_TO_Z4:
            return
        if not self.testIfZoneFree(Zone.Z5) and not self.testIfPalletWithStatusExist(PalletStatus.MOVING_TO_Z5):
            pallet.status = PalletStatus.MOVING_TO_Z5
            self.ws.conveyor.movePallet(Zone.Z4, Zone.Z5)

    def printPalletInfo(self):
        print("Pallets: ")
        for p in self.ws.pallets:
            p.printPalletInfo()

    def testFinalStatus(self):
        for p in self.ws.pallets:
            if p.status is PalletStatus.MOVING_TO_Z2 or p.status is PalletStatus.MOVING_TO_Z3 or p.status is PalletStatus.MOVING_TO_Z4 or p.status is PalletStatus.MOVING_TO_Z5 or p.status is PalletStatus.DRAWING:
                self.status.changeLightColor(StatusCode.WORKING)
                return
        self.status.changeLightColor(StatusCode.IDLE)
