"""STUDENT FILE. Implement the search state machine. No ROS calls in this module.
Use raster() and drive_to(); never read simulator internals or web /state.
Return Outcome('absent') ONLY after covering the entire requested area.
Return Outcome('found', x, y) after measuring the rectangle centre.
"""
from course_lab.world import Area, Sample, Decision
from course_lab.navigation import drive_to, raster
from course_lab.probe import RectangleProbe


from course_lab.world import Area, Sample, Decision, Outcome
from course_lab.navigation import drive_to, raster
from course_lab.probe import RectangleProbe


class Mission:
    def __init__(self, area: Area):
        self.area = area
        self.waypoints = raster(area)
        self.index = 0
        self.probe = None

    def step(self, sample: Sample) -> Decision:
        if self.probe is not None:
            return self.probe.step(sample)

        if sample.green and self.area.contains(sample.x, sample.y):
            self.probe = RectangleProbe(self.area, sample)
            return Decision(detected=True)

        if self.index >= len(self.waypoints):
            return Decision(
                outcome=Outcome("absent")
            )

        target = self.waypoints[self.index]
        v, w, reached = drive_to(sample, target)
        if reached:
            self.index += 1

            if self.index >= len(self.waypoints):
                return Decision(
                    outcome=Outcome("absent")
                )

            return Decision()
        return Decision(v=v, w=w)


