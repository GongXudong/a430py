import unittest

from a430py.simulator.a430_sim import A430Simulator


class A430SimulatorTest(unittest.TestCase):
    def test_init(
        self,
    ):
        self.sim = A430Simulator(config={})
        self.sim.set_init_info(
            dLon=120,
            dLat=30,
            fAlt=10,
            fTAS=90,
            fYaw=90,
        )
        self.sim.init_plane_model()

    def test_trajectory_2(self):
        print("In test trajectory 2 with plane initialized with default configs: ")

        self.sim = A430Simulator(config={})

        self.sim.init_plane_model(
            dLon=120,
            dLat=30,
            fAlt=10,
            fTAS=90,
            fYaw=90,
        )

        for i in range(60):
            next_state = self.sim.step(
                fStickLat=0.0,
                fStickLon=-1.998228,
                fThrottle=0.689030,
                fRudder=0,
            )
            # print(f"next_state = {next_state}")

    def test_trajectory_3(self):
        print("In test trajectory 3 with plane initialized with customized configs: ")
        custom_config = {
            "m": 0.1,
        }
        self.sim = A430Simulator(config=custom_config)
        print(f"check config: m = {self.sim.get_config()['m']}")

        self.sim.init_plane_model(
            dLon=120,
            dLat=30,
            fAlt=10,
            fTAS=8,
            fYaw=90,
        )

        for i in range(60):
            next_state = self.sim.step(
                fStickLat=0.0,
                fStickLon=-1.998228,
                fThrottle=0.689030,
                fRudder=0,
            )
            # print(f"next_state = {next_state}")

    def test_reset_1(self):
        print("In test reset 1: ")
        custom_config = {
            "m": 0.1,
        }
        self.sim = A430Simulator(config=custom_config)
        print(f"check config: m = {self.sim.get_config()['m']}")

        self.sim.init_plane_model(
            dLon=120,
            dLat=30,
            fAlt=10,
            fTAS=8,
            fYaw=90,
        )

        for i in range(60):
            next_state = self.sim.step(
                fStickLat=0.0,
                fStickLon=-1.998228,
                fThrottle=0.689030,
                fRudder=0,
            )

        self.sim.reset(
            dLon=120,
            dLat=30,
            fAlt=10,
            fTAS=90,
            fYaw=90,
        )

        for i in range(60):
            next_state = self.sim.step(
                fStickLat=0.0,
                fStickLon=-1.998228,
                fThrottle=0.689030,
                fRudder=0,
            )
            print(f"next_state = {next_state}")

    # def test_trajectory_1(self):
    #     self.sim = A430Simulator(config={})

    #     self.sim.init_plane_model(
    #         dLon=120,
    #         dLat=30,
    #         fAlt=10,
    #         fTAS=8,
    #         fYaw=90,
    #     )

    #     # 实例输入
    #     self.sim.set_aircraft_input(
    #         fStickLat=0.0,
    #         fStickLon=-1.998228,
    #         fThrottle=0.689030,
    #         fRudder=0,
    #     )
    #     self.sim.a430_model.set_input(self.sim.planePtr, self.sim.aircraft_input)

    #     # 定义实例输出
    #     acmi = AcmiLogger("trace.acmi")

    #     logheads = 'time'
    #     for i,item in enumerate(self.sim.aircraft_output._fields_):
    #         logheads += ','
    #         logheads += item[0]
    #     logheads += "\n"

    #     with open("./trace.csv", "w") as log:
    #         log.write(logheads)
    #         planeID = 101
    #         for i in range(60):
    #             self.sim.a430_model.update(self.sim.planePtr)     # 更新飞机状态
    #             self.sim.a430_model.get_output(self.sim.planePtr, byref(self.sim.aircraft_output))   # 读取飞机输出状态
    #             print(self.sim.get_aircraft_output())
    #             acmi.writeTime(i * self.sim.step_time)
    #             acmi.writeOnePlane(planeID, self.sim.aircraft_output.dLon, self.sim.aircraft_output.dLat, self.sim.aircraft_output.fAlt, self.sim.aircraft_output.fRoll, self.sim.aircraft_output.fPitch, self.sim.aircraft_output.fYaw, i==0)
    #             log.write(str(i * self.sim.step_time))
    #             for field_name, _ in self.sim.aircraft_output._fields_:
    #                 value = getattr(self.sim.aircraft_output, field_name)
    #                 log.write(",")
    #                 log.write(str(value))
    #             log.write("\n")

    #     self.sim.close()

    # def test_single_step_1(self,):
    #     custom_config = {
    #         "m": 0.1,
    #     }
    #     self.sim = A430Simulator(config=custom_config)
    #     print(f"check config: m = {self.sim.get_config()['m']}")

    #     self.sim.init_plane_model(
    #         dLon=120,
    #         dLat=30,
    #         fAlt=10,
    #         fTAS=8,
    #         fYaw=90,
    #     )

    #     # 实例输入
    #     self.sim.set_aircraft_input(
    #         fStickLat=0.0,
    #         fStickLon=-1.998228,
    #         fThrottle=0.689030,
    #         fRudder=0,
    #     )
    #     self.sim.a430_model.set_input(self.sim.planePtr, self.sim.aircraft_input)

    #     self.sim.set_aircraft_state(
    #         vt=9, alpha=2, beta=0,
    #         phi=0, theta=0, psi=0,
    #         p=0, q=0, r=0, h=0,
    #     )
    #     self.sim.a430_model.set_state(self.sim.planePtr, self.sim.aircraft_state)
    #     self.sim.a430_model.get_output(self.sim.planePtr, byref(self.sim.aircraft_output))
    #     print('output1')
    #     # showOutput(output1)
    #     self.sim.showOutputInDictFormat(self.sim.aircraft_output)
    #     # self.sim.a430_model.get_delta(self.sim.planePtr, byref(self.sim.aircraft_output_delta))
    #     # print('delta1')
    #     # self.sim.showOutputInDictFormat(self.sim.aircraft_output_delta)

    #     for i in range(10):

    #         print("\nBefore update")
    #         self.sim.a430_model.update(self.sim.planePtr)
    #         print("After Update\n")

    #         self.sim.a430_model.get_output(self.sim.planePtr, byref(self.sim.aircraft_output))
    #         print(f'output{2+i}')
    #         self.sim.showOutputInDictFormat(self.sim.aircraft_output)
    #         # self.sim.a430_model.get_delta(self.sim.planePtr, byref(self.sim.aircraft_output_delta))
    #         # print(f'delta{2+i}')
    #         # self.sim.showOutputInDictFormat(self.sim.aircraft_output_delta)

    #     self.sim.a430_model.terminate_plane(self.sim.planePtr)  # 飞机销毁

    # def test_1(self):
    #     self.sim = A430Simulator(config={})
    #     self.sim.test_delta()


if __name__ == "__main__":
    unittest.main()
