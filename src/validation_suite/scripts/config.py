IMU_RANGES = {
    "orientation": {
        "good":  {"roll": (-15, 15),  "pitch": (-20, 20),  "yaw": (-180, 180)},
        "warn":  {"roll": (-30, 30),  "pitch": (-35, 35),  "yaw": (-180, 180)},
        "poor":  {"roll": (-90, 90),  "pitch": (-90, 90),  "yaw": (-180, 180)}
    },
    "angular_velocity": {
        "good":  {"x": (-2, 2),   "y": (-2, 2),   "z": (-2, 2)},
        "warn":  {"x": (-5, 5),   "y": (-5, 5),   "z": (-5, 5)},
        "poor":  {"x": (-15, 15), "y": (-15, 15), "z": (-15, 15)}
    },
    "linear_acceleration": {
        "good":  {"x": (-15, 15), "y": (-15, 15), "z": (5, 15)},
        "warn":  {"x": (-20, 20), "y": (-20, 20), "z": (2, 20)},
        "poor":  {"x": (-50, 50), "y": (-50, 50), "z": (-50, 50)}
    }
}

POSE_WITH_COVARIANCE_RANGES = {
    "position": {
        "good": {
            "x": (-20.0, 20.0),
            "y": (-20.0, 20.0),
            "z": (-2.0, 2.0),
        },
        "warn": {
            "x": (-50.0, 50.0),
            "y": (-50.0, 50.0),
            "z": (-5.0, 5.0),
        },
        "poor": {
            "x": (-100.0, 100.0),
            "y": (-100.0, 100.0),
            "z": (-20.0, 20.0),
        },
    },

    # Diagonal covariance entries:
    # x -> cov[0]
    # y -> cov[7]
    # z -> cov[14]
    "position_covariance": {
        "good": (0.0, 0.05),
        "warn": (0.05, 0.20),
        "poor": (0.20, 1.00),
    },

    # roll -> cov[21]
    # pitch -> cov[28]
    # yaw -> cov[35]
    "orientation_covariance": {
        "good": (0.0, 0.01),
        "warn": (0.01, 0.05),
        "poor": (0.05, 0.50),
    },
}

TWIST_WITH_COVARIANCE_RANGES = {
    "linear_velocity": {
        "good": {
            "x": (-2.0, 2.0),
            "y": (-2.0, 2.0),
            "z": (-1.0, 1.0),
        },
        "warn": {
            "x": (-5.0, 5.0),
            "y": (-5.0, 5.0),
            "z": (-2.0, 2.0),
        },
        "poor": {
            "x": (-15.0, 15.0),
            "y": (-15.0, 15.0),
            "z": (-5.0, 5.0),
        },
    },

    "angular_velocity": {
        "good": {
            "x": (-2.0, 2.0),
            "y": (-2.0, 2.0),
            "z": (-2.0, 2.0),
        },
        "warn": {
            "x": (-5.0, 5.0),
            "y": (-5.0, 5.0),
            "z": (-5.0, 5.0),
        },
        "poor": {
            "x": (-15.0, 15.0),
            "y": (-15.0, 15.0),
            "z": (-15.0, 15.0),
        },
    },

    # linear.x -> cov[0]
    # linear.y -> cov[7]
    # linear.z -> cov[14]
    "linear_covariance": {
        "good": (0.0, 0.05),
        "warn": (0.05, 0.20),
        "poor": (0.20, 1.00),
    },

    # angular.x -> cov[21]
    # angular.y -> cov[28]
    # angular.z -> cov[35]
    "angular_covariance": {
        "good": (0.0, 0.01),
        "warn": (0.01, 0.05),
        "poor": (0.05, 0.50),
    },
}