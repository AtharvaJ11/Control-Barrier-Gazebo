;; Auto-generated. Do not edit!


(when (boundp 'cbf_simulation::cbf_data)
  (if (not (find-package "CBF_SIMULATION"))
    (make-package "CBF_SIMULATION"))
  (shadow 'cbf_data (find-package "CBF_SIMULATION")))
(unless (find-package "CBF_SIMULATION::CBF_DATA")
  (make-package "CBF_SIMULATION::CBF_DATA"))

(in-package "ROS")
;;//! \htmlinclude cbf_data.msg.html


(defclass cbf_simulation::cbf_data
  :super ros::object
  :slots (_stamp _px _py _vx _vy _ux_nom _uy_nom _ux_safe _uy_safe ))

(defmethod cbf_simulation::cbf_data
  (:init
   (&key
    ((:stamp __stamp) (instance ros::time :init))
    ((:px __px) 0.0)
    ((:py __py) 0.0)
    ((:vx __vx) 0.0)
    ((:vy __vy) 0.0)
    ((:ux_nom __ux_nom) 0.0)
    ((:uy_nom __uy_nom) 0.0)
    ((:ux_safe __ux_safe) 0.0)
    ((:uy_safe __uy_safe) 0.0)
    )
   (send-super :init)
   (setq _stamp __stamp)
   (setq _px (float __px))
   (setq _py (float __py))
   (setq _vx (float __vx))
   (setq _vy (float __vy))
   (setq _ux_nom (float __ux_nom))
   (setq _uy_nom (float __uy_nom))
   (setq _ux_safe (float __ux_safe))
   (setq _uy_safe (float __uy_safe))
   self)
  (:stamp
   (&optional __stamp)
   (if __stamp (setq _stamp __stamp)) _stamp)
  (:px
   (&optional __px)
   (if __px (setq _px __px)) _px)
  (:py
   (&optional __py)
   (if __py (setq _py __py)) _py)
  (:vx
   (&optional __vx)
   (if __vx (setq _vx __vx)) _vx)
  (:vy
   (&optional __vy)
   (if __vy (setq _vy __vy)) _vy)
  (:ux_nom
   (&optional __ux_nom)
   (if __ux_nom (setq _ux_nom __ux_nom)) _ux_nom)
  (:uy_nom
   (&optional __uy_nom)
   (if __uy_nom (setq _uy_nom __uy_nom)) _uy_nom)
  (:ux_safe
   (&optional __ux_safe)
   (if __ux_safe (setq _ux_safe __ux_safe)) _ux_safe)
  (:uy_safe
   (&optional __uy_safe)
   (if __uy_safe (setq _uy_safe __uy_safe)) _uy_safe)
  (:serialization-length
   ()
   (+
    ;; time _stamp
    8
    ;; float64 _px
    8
    ;; float64 _py
    8
    ;; float64 _vx
    8
    ;; float64 _vy
    8
    ;; float64 _ux_nom
    8
    ;; float64 _uy_nom
    8
    ;; float64 _ux_safe
    8
    ;; float64 _uy_safe
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; time _stamp
       (write-long (send _stamp :sec) s) (write-long (send _stamp :nsec) s)
     ;; float64 _px
       (sys::poke _px (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _py
       (sys::poke _py (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _vx
       (sys::poke _vx (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _vy
       (sys::poke _vy (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _ux_nom
       (sys::poke _ux_nom (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _uy_nom
       (sys::poke _uy_nom (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _ux_safe
       (sys::poke _ux_safe (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _uy_safe
       (sys::poke _uy_safe (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; time _stamp
     (send _stamp :sec (sys::peek buf ptr- :integer)) (incf ptr- 4)  (send _stamp :nsec (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; float64 _px
     (setq _px (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _py
     (setq _py (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _vx
     (setq _vx (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _vy
     (setq _vy (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _ux_nom
     (setq _ux_nom (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _uy_nom
     (setq _uy_nom (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _ux_safe
     (setq _ux_safe (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _uy_safe
     (setq _uy_safe (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get cbf_simulation::cbf_data :md5sum-) "c9f6db06237f3b61c11f2d3385758187")
(setf (get cbf_simulation::cbf_data :datatype-) "cbf_simulation/cbf_data")
(setf (get cbf_simulation::cbf_data :definition-)
      "time stamp
float64 px
float64 py
float64 vx
float64 vy
float64 ux_nom
float64 uy_nom
float64 ux_safe
float64 uy_safe
")



(provide :cbf_simulation/cbf_data "c9f6db06237f3b61c11f2d3385758187")


