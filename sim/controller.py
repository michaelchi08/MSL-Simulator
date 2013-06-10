# Python imports
import sys
import math

# PySide imports
from PySide import QtGui, QtCore

# MSL Sim imports
import sim.model as mod
import sim.defaults as d


class MainWindow(QtGui.QMainWindow):
    """The main window. This window displays all the widgets."""
    def __init__(self):
        super(MainWindow, self).__init__()
        self.robot = mod.Robot()
        self.loadGUI()
        # Place and scale the logo
        pixmap = QtGui.QPixmap("msl_logo.png")
        self.ui.logo_label.setPixmap(pixmap)
        # Give the zoomed in plotting area the same scene as the zoomed out one
        self.ui.graphics_view_zoom.setScene(self.ui.graphics_view.scene())
        # Initialize the camera in the zoomed in plotting window
        self.ui.graphics_view_zoom.initializeCamera(self.robot)
        # Give the zoomed-out plotting area a copy of the zoomed-in plotting
        # area so it can change it based on its timers
        self.ui.graphics_view.zoom = self.ui.graphics_view_zoom
        # Give the plotting area the same robot as the rest of the GUI and start
        # updating it via timers
        self.ui.graphics_view.robot = self.robot
        self.ui.graphics_view.initialiseRobot()
        self.settings_to_default()
        # Start a timer that updates the labels
        self.label_timer = QtCore.QTimer()
        self.label_timer.timeout.connect(self.update_info_labels)
        self.label_timer.start()
        # Start timers that update the plot and the model
        self.ui.graphics_view.start_timers()

    def loadGUI(self):
        """Load the GUI from the .py file that was generated by the .ui file
        using the pyside-uic tool."""
        # import generated .py file here to prevent circular reference
        from sim.view import Ui_main_window
        self.ui = Ui_main_window()
        self.ui.setupUi(self)
        self.connect_signals_to_slots()
        # Add items to pull down menus
        self.ui.laser_combo.addItems(["Custom", "SICK LMS111",
            "Hokuyo URG-04LX"])
        self.ui.robot_combo.addItems(["Custom", "Clearpath Husky A200",
            "MobileRobots P3AT"])

    def update_info_labels(self):
        self.ui.pose_label.setText("%0.2f m, %0.2f m, %d deg" % (self.robot.x,
                self.robot.y, 180/math.pi*self.robot.heading))
        self.ui.velocity_label.setText("%0.2f m/s" % self.robot.vel)
        self.ui.ang_vel_label.setText("%d deg/s" % int(180/math.pi*self.robot.ang_vel))

    def toggle_enable_laser_settings(self, b):
        self.ui.laser_range_slider.setEnabled(b)
        self.ui.laser_range_box.setEnabled(b)
        self.ui.laser_fov_slider.setEnabled(b)
        self.ui.laser_fov_box.setEnabled(b)
        self.ui.laser_res_slider.setEnabled(b)
        self.ui.laser_res_box.setEnabled(b)
        self.ui.laser_freq_slider.setEnabled(b)
        self.ui.laser_freq_box.setEnabled(b)
        self.ui.laser_noise_slider.setEnabled(b)
        self.ui.laser_noise_box.setEnabled(b)

    def toggle_enable_robot_settings(self, b):
        self.ui.robot_length_slider.setEnabled(b)
        self.ui.robot_length_box.setEnabled(b)
        self.ui.robot_width_slider.setEnabled(b)
        self.ui.robot_width_box.setEnabled(b)
        self.ui.robot_wheel_rad_slider.setEnabled(b)
        self.ui.robot_wheel_rad_box.setEnabled(b)
        self.ui.robot_wheelbase_slider.setEnabled(b)
        self.ui.robot_wheelbase_box.setEnabled(b)
        self.ui.robot_vel_slider.setEnabled(b)
        self.ui.robot_vel_box.setEnabled(b)
        self.ui.robot_ang_vel_slider.setEnabled(b)
        self.ui.robot_ang_vel_box.setEnabled(b)

    def connect_signals_to_slots(self):
        # -----
        # ROBOT
        # -----
        self.ui.robot_combo.currentIndexChanged.connect(self.robot_combo_changed)
        self.ui.robot_length_slider.valueChanged.connect(
                lambda: self.robot_length_changed(
                    self.ui.robot_length_slider.value()/10.0))
        self.ui.robot_length_box.valueChanged.connect(
                self.robot_length_changed)
        self.ui.robot_width_slider.valueChanged.connect(
                lambda: self.robot_width_changed(
                    self.ui.robot_width_slider.value()/10.0))
        self.ui.robot_width_box.valueChanged.connect(
                self.robot_width_changed)
        self.ui.robot_wheel_rad_slider.valueChanged.connect(
                lambda: self.robot_wheel_rad_changed(
                    self.ui.robot_wheel_rad_slider.value()/100.0))
        self.ui.robot_wheel_rad_box.valueChanged.connect(
                self.robot_wheel_rad_changed)
        self.ui.robot_wheelbase_slider.valueChanged.connect(
                lambda: self.robot_wheelbase_changed(
                    self.ui.robot_wheelbase_slider.value()/10.0))
        self.ui.robot_wheelbase_box.valueChanged.connect(
                self.robot_wheelbase_changed)
        self.ui.robot_vel_slider.valueChanged.connect(
                lambda: self.robot_vel_changed(
                    self.ui.robot_vel_slider.value()/10.0))
        self.ui.robot_vel_box.valueChanged.connect(self.robot_vel_changed)
        self.ui.robot_ang_vel_slider.valueChanged.connect(
                self.robot_ang_vel_changed)
        self.ui.robot_ang_vel_box.valueChanged.connect(
                self.robot_ang_vel_changed)

        # --------
        # ODOMETER
        # --------

        # -----
        # LASER
        # -----
        self.ui.laser_combo.currentIndexChanged.connect(self.laser_combo_changed)
        self.ui.laser_range_slider.valueChanged.connect(
                self.laser_range_changed)
        self.ui.laser_range_box.valueChanged.connect(
                self.laser_range_changed)
        self.ui.laser_fov_slider.valueChanged.connect(
                self.laser_fov_changed)
        self.ui.laser_fov_box.valueChanged.connect(
                self.laser_fov_changed)
        self.ui.laser_res_slider.valueChanged.connect(
                lambda: self.laser_res_changed(self.ui.laser_res_slider.value()/10.0))
        self.ui.laser_res_box.valueChanged.connect(
                self.laser_res_changed)
        self.ui.laser_freq_slider.valueChanged.connect(
                self.laser_freq_changed)
        self.ui.laser_freq_box.valueChanged.connect(
                self.laser_freq_changed)
        self.ui.laser_noise_slider.valueChanged.connect(
                self.laser_noise_changed)
        self.ui.laser_noise_box.valueChanged.connect(
                self.laser_noise_changed)

        # -----
        # OTHER
        # -----
        self.ui.vel_inc_box.valueChanged.connect(self.vel_inc_changed)
        self.ui.ang_vel_inc_box.valueChanged.connect(self.ang_vel_inc_changed)

    def settings_to_default(self):
        # -----
        # ROBOT
        # -----
        self.robot_length_changed(d.ROBOT_LENGTH)
        self.robot_width_changed(d.ROBOT_WIDTH)
        self.robot_wheel_rad_changed(d.ROBOT_WHEEL_RAD)
        self.robot_wheelbase_changed(d.ROBOT_WHEELBASE)
        self.robot_vel_changed(d.ROBOT_MAX_VEL)
        self.robot_ang_vel_changed(d.ROBOT_MAX_ANG_VEL)

        # --------
        # ODOMETER
        # --------

        # -----
        # LASER
        # -----
        self.laser_range_changed(d.LASER_RANGE)
        self.laser_fov_changed(d.LASER_MAX_ANGLE - d.LASER_MIN_ANGLE)
        self.laser_res_changed(d.LASER_RES)
        self.laser_freq_changed(d.LASER_FREQ)
        self.laser_noise_changed(d.LASER_NOISE)

        # -----
        # OTHER
        # -----
        self.vel_inc_changed(d.VELOCITY_INCREMENT)
        self.ang_vel_inc_changed(d.ANG_VELOCITY_INCREMENT)

    # --------------------------------------------------------------------------
    # SLOTS
    # --------------------------------------------------------------------------

    # -----
    # ROBOT
    # -----
    def robot_combo_changed(self, value):
        if value == 0: # Custom
            self.toggle_enable_robot_settings(True)
        elif value == 1: # Clearpath Husky A200
            self.robot_length_changed(d.HUSKY_LENGTH)
            self.robot_width_changed(d.HUSKY_WIDTH)
            self.robot_wheel_rad_changed(d.HUSKY_WHEEL_RAD)
            self.robot_wheelbase_changed(d.HUSKY_WHEELBASE)
            self.robot_vel_changed(d.HUSKY_MAX_VEL)
            self.robot_ang_vel_changed(d.HUSKY_MAX_ANG_VEL)
            self.toggle_enable_robot_settings(False)
        elif value == 2: # MobileRobots P3AT
            self.robot_length_changed(d.P3AT_LENGTH)
            self.robot_width_changed(d.P3AT_WIDTH)
            self.robot_wheel_rad_changed(d.P3AT_WHEEL_RAD)
            self.robot_wheelbase_changed(d.P3AT_WHEELBASE)
            self.robot_vel_changed(d.P3AT_MAX_VEL)
            self.robot_ang_vel_changed(d.P3AT_MAX_ANG_VEL)
            self.toggle_enable_robot_settings(False)

    def robot_length_changed(self, value):
        self.ui.robot_length_slider.setValue(int(10*value))
        self.ui.robot_length_box.setValue(value)
        self.robot.set_length(value)

    def robot_width_changed(self, value):
        self.ui.robot_width_slider.setValue(int(10*value))
        self.ui.robot_width_box.setValue(value)
        self.robot.set_width(value)

    def robot_wheel_rad_changed(self, value):
        self.ui.robot_wheel_rad_slider.setValue(int(100*value))
        self.ui.robot_wheel_rad_box.setValue(value)
        self.robot.set_wheel_rad(value)

    def robot_wheelbase_changed(self, value):
        self.ui.robot_wheelbase_slider.setValue(int(10*value))
        self.ui.robot_wheelbase_box.setValue(value)
        self.robot.set_wheelbase(value)

    def robot_vel_changed(self, value):
        self.ui.robot_vel_slider.setValue(int(10*value))
        self.ui.robot_vel_box.setValue(value)
        self.robot.max_vel = value

    def robot_ang_vel_changed(self, value):
        self.ui.robot_ang_vel_slider.setValue(value)
        self.ui.robot_ang_vel_box.setValue(value)
        self.robot.max_ang_vel = value * math.pi/180

    # --------
    # ODOMETER
    # --------

    # -----
    # LASER
    # -----
    def laser_combo_changed(self, value):
        if value == 0: # Custom
            self.toggle_enable_laser_settings(True)
        elif value == 1: # SICK LMS111
            self.laser_range_changed(d.SICK_111_RANGE)
            self.laser_fov_changed(
                    (d.SICK_111_MAX_ANGLE - d.SICK_111_MIN_ANGLE))
            self.laser_res_changed(d.SICK_111_RES)
            self.laser_freq_changed(d.SICK_111_FREQ)
            self.laser_noise_changed(d.SICK_111_NOISE)
            self.toggle_enable_laser_settings(False)
        elif value == 2: # Hokuyo URG-04LX
            self.laser_range_changed(d.HOK_04_RANGE)
            self.laser_fov_changed(
                    (d.HOK_04_MAX_ANGLE - d.HOK_04_MIN_ANGLE))
            self.laser_res_changed(d.HOK_04_RES)
            self.laser_freq_changed(d.HOK_04_FREQ)
            self.laser_noise_changed(d.HOK_04_NOISE)
            self.toggle_enable_laser_settings(False)

    def laser_range_changed(self, value):
        self.ui.laser_range_box.setValue(value)
        self.ui.laser_range_slider.setValue(value)
        self.robot.laser.range = value

    def laser_fov_changed(self, value):
        self.ui.laser_fov_box.setValue(value)
        self.ui.laser_fov_slider.setValue(value)
        self.robot.laser.min_angle = -value/2.0
        self.robot.laser.max_angle = value/2.0

    def laser_res_changed(self, value):
        self.ui.laser_res_slider.setValue(int(10*value))
        self.ui.laser_res_box.setValue(value)
        self.robot.laser.resolution = value

    def laser_freq_changed(self, value):
        self.ui.laser_freq_slider.setValue(value)
        self.ui.laser_freq_box.setValue(value)
        self.robot.laser.freq = value
        self.ui.graphics_view.set_timer_frequencies()

    def laser_noise_changed(self, value):
        self.ui.laser_noise_slider.setValue(value)
        self.ui.laser_noise_box.setValue(value)
        self.robot.laser.noise = value/100.0 # convert to metres

    # -----
    # OTHER
    # -----
    def vel_inc_changed(self, value):
        self.ui.vel_inc_box.setValue(value)
        self.vel_inc = value

    def ang_vel_inc_changed(self, value):
        self.ui.ang_vel_inc_box.setValue(value)
        self.ang_vel_inc = value

    def keyPressEvent(self, event):
        """Adjusts the translational and angular velocites of the robot. Does
        not allow the velocities to go beyond the maximum and minimums. Sets
        the velocities to zero at zero-crossings (sign changes)."""
        vel_inc = self.vel_inc
        ang_vel_inc = self.ang_vel_inc * math.pi/180

        # W KEY PRESSED: INCREASE VELOCITY
        if event.key() == QtCore.Qt.Key_W:
            # Go to zero on sign changes
            if self.robot.vel < 0 and self.robot.vel + vel_inc > 0:
                self.robot.vel = 0
            # Change only if limit is not exceeded
            elif self.robot.vel < self.robot.max_vel:
                # Go to limit if increment would go beyond it
                if self.robot.vel + vel_inc > self.robot.max_vel:
                    self.robot.vel = self.robot.max_vel
                else:
                    self.robot.vel += vel_inc
                
        # S KEY PRESSED: DECREASE VELOCITY
        elif event.key() == QtCore.Qt.Key_S:
            # Go to zero on sign changes
            if self.robot.vel > 0 and self.robot.vel - vel_inc < 0:
                self.robot.vel = 0
            # Change only if limit is not exceeded
            elif self.robot.vel > -self.robot.max_vel:
                # Go to limit if increment would go beyond it
                if self.robot.vel - vel_inc < -self.robot.max_vel:
                    self.robot.vel = -self.robot.max_vel
                else:
                    self.robot.vel -= vel_inc

        # A KEY PRESSED: INCREASE ANGULAR VELOCITY
        elif event.key() == QtCore.Qt.Key_A:
            # Go to zero on sign changes
            if self.robot.ang_vel < 0 and self.robot.ang_vel + ang_vel_inc > 0:
                self.robot.ang_vel = 0
            # Change only if limit is not exceeded
            elif self.robot.ang_vel < self.robot.max_ang_vel:
                # Go to limit if increment would go beyond it
                if (self.robot.ang_vel + ang_vel_inc > self.robot.max_ang_vel):
                    self.robot.ang_vel = self.robot.max_ang_vel
                else:
                    self.robot.ang_vel += ang_vel_inc

        # D KEY PRESSED: DECREASE ANGULAR VELOCITY
        elif event.key() == QtCore.Qt.Key_D:
            # Go to zero on sign changes
            if self.robot.ang_vel > 0 and self.robot.ang_vel - ang_vel_inc < 0:
                self.robot.ang_vel = 0
            # Change only if limit is not exceeded
            elif self.robot.ang_vel > -self.robot.max_ang_vel:
                # Go to limit if increment would go beyond it
                if (self.robot.ang_vel - ang_vel_inc < -self.robot.max_ang_vel):
                    self.robot.ang_vel = -self.robot.max_ang_vel
                else:
                    self.robot.ang_vel -= ang_vel_inc


class PlotGraphicsView(QtGui.QGraphicsView):
    def __init__(self, parent):
        super(PlotGraphicsView, self).__init__(parent)
        self.parent = parent
        self.plot_freq = d.PLOT_FREQ
        self.line_map = []
        self.scale(20, -20)
        self.scan_list = []
        self.set_colours()
        self.g_scene = QtGui.QGraphicsScene(self)
        self.setScene(self.g_scene)
        self.setSceneRect(-d.MAP_WIDTH/2.0, -d.MAP_HEIGHT/2.0, d.MAP_WIDTH,
                d.MAP_HEIGHT)
        self.plot_timer = QtCore.QTimer()
        self.odom_timer = QtCore.QTimer()
        self.laser_timer = QtCore.QTimer()

    def initialiseRobot(self):
        """Draws the robot in the scene."""
        self.rect = self.scene().addRect(self.robot.x - self.robot.length/2.0,
                                         self.robot.y - self.robot.width/2.0,
                                         self.robot.length, self.robot.width,
                                         self.robot_pen)
        self.rect.setTransformOriginPoint(self.robot.x,
                                          self.robot.y)
        self.previous_pose = self.robot.pose

    def start_timers(self):
        """Starts separate timers to update the plot, odometry, and range data
        from the laser."""
        self.set_timer_frequencies()
        self.plot_timer.timeout.connect(self.plot_update)
        self.odom_timer.timeout.connect(self.robot.update_pose)
        self.laser_timer.timeout.connect(
                lambda: self.robot.scan_laser(self.line_map))
        self.plot_timer.start()
        self.odom_timer.start()
        self.laser_timer.start()

    def set_colours(self):
        """Creates QPen instances for all the objects that will be plotted."""
        self.laser_pen = QtGui.QPen()
        self.robot_pen = QtGui.QPen()
        red = QtGui.QColor(255, 0, 0)
        green = QtGui.QColor(0, 255, 0)
        red.setAlpha(40)
        self.laser_pen.setColor(red)
        self.robot_pen.setColor(green)

    def plot_update(self):
        """Updates the plot. This method is called automatically by the
        plot_timer."""
        # Size of robot in plot
        if self.robot.changed:
            self.rect.setRect(self.robot.x - self.robot.length/2.0,
                    self.robot.y - self.robot.width/2.0,
                    self.robot.length, self.robot.width)
            self.rect.setTransformOriginPoint(self.robot.x,
                                              self.robot.y)
            self.rect.setRotation(180/math.pi * self.robot.heading)
            # Camera pose for zoomed in view
            self.move_zoomed_view()
            # Reset flag
            self.robot.changed = False
        # Laser beams
        if self.robot.scanned:
            self.draw_laser_beams(self.robot.last_scan)
            # Reset flag
            self.robot.scanned = False

    def set_timer_frequencies(self):
        self.plot_timer.setInterval(1000.0/self.plot_freq)
        self.odom_timer.setInterval(1000.0/self.robot.odometer.freq)
        self.laser_timer.setInterval(1000.0/self.robot.laser.freq)

    def move_zoomed_view(self):
        # Adjust the window of the zoomed in view
        self.zoom.setSceneRect(self.robot.x - self.robot.length/2.0, 
                self.robot.y - self.robot.width/2.0, 
                self.robot.length, self.robot.width)
        heading_change = 180/math.pi * (self.previous_pose[2] - self.robot.heading)
        self.zoom.rotate(heading_change)
        self.previous_pose = self.robot.pose

    def draw_laser_beams(self, scan):
        """Deletes any previously drawn laser beams and plots the latest laser
        measurement."""
        pose, ranges = scan
        x, y, theta = self.robot.pose
        laser_range = self.robot.laser.range
        laser_min_angle = self.robot.laser.min_angle
        laser_res = self.robot.laser.resolution
        # Empty out the scan group
        if self.scan_list:
            for item in self.scan_list:
                self.scene().removeItem(item)
            self.scan_list = []
        for (i, r) in enumerate(ranges):
            if r == 0:
                r = laser_range
            x_2 = x + math.pi/180 + r*math.cos(
                    theta + math.pi/180*(laser_min_angle + laser_res*i))
            y_2 = y + math.pi/180 + r*math.sin(
                    theta + math.pi/180*(laser_min_angle + laser_res*i))
            self.scan_list.append(
                    self.scene().addLine(QtCore.QLineF(x, y, x_2, y_2), self.laser_pen))

    def mousePressEvent(self, event):
        """Records the coordinates of the point where the mouse was clicked on
        the scene."""
        if event.button() == QtCore.Qt.LeftButton:
            self.start = QtCore.QPointF(self.mapToScene(event.pos()))

    def mouseReleaseEvent(self, event):
        """Draws a line from the recorded click coordinates and the position of 
        the cursor when the left mouse button is released. Adds this line to
        the line map."""
        if event.button() == QtCore.Qt.LeftButton:
            end = QtCore.QPointF(self.mapToScene(event.pos()))
            line = mod.get_line_dict(self.start.x(), self.start.y(),
                    end.x(), end.y())
            self.line_map.append(line)
            self.scene().addItem(
                    QtGui.QGraphicsLineItem(QtCore.QLineF(self.start, end)))


class PlotGraphicsViewZoom(QtGui.QGraphicsView):
    def __init__(self, parent):
        super(PlotGraphicsViewZoom, self).__init__(parent)
        self.parent = parent
        self.scale(40, -40)

    def initializeCamera(self, robot):
        self.setSceneRect(robot.x - robot.length/2.0, robot.y - robot.width/2.0,
                robot.length, robot.width)
        self.rotate(90)
