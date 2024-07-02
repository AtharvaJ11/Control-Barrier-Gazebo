;; Auto-generated. Do not edit!


(when (boundp 'cbf_simulation::state_msg)
  (if (not (find-package "CBF_SIMULATION"))
    (make-package "CBF_SIMULATION"))
  (shadow 'state_msg (find-package "CBF_SIMULATION")))
(unless (find-package "CBF_SIMULATION::STATE_MSG")
  (make-package "CBF_SIMULATION::STATE_MSG"))

(in-package "ROS")
;;//! \htmlinclude state_msg.msg.html


(defclass cbf_simulation::state_msg
  :super ros::object
  :slots (_id _x _y _vx _vy ))

(defmethod cbf_simulation::state_msg
  (:init
   (&key
    ((:id __id) 0)
    ((:x __x) 0.0)
    ((:y __y) 0.0)
    ((:vx __vx) 0.0)
    ((:vy __vy) 0.0)
    )
   (send-super :init)
   (setq _id (round __id))
   (setq _x (float __x))
   (setq _y (float __y))
   (setq _vx (float __vx))
   (setq _vy (float __vy))
   self)
  (:id
   (&optional __id)
   (if __id (setq _id __id)) _id)
  (:x
   (&optional __x)
   (if __x (setq _x __x)) _x)
  (:y
   (&optional __y)
   (if __y (setq _y __y)) _y)
  (:vx
   (&optional __vx)
   (if __vx (setq _vx __vx)) _vx)
  (:vy
   (&optional __vy)
   (if __vy (setq _vy __vy)) _vy)
  (:serialization-length
   ()
   (+
    ;; int8 _id
    1
    ;; float64 _x
    8
    ;; float64 _y
    8
    ;; float64 _vx
    8
    ;; float64 _vy
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int8 _id
       (write-byte _id s)
     ;; float64 _x
       (sys::poke _x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _y
       (sys::poke _y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _vx
       (sys::poke _vx (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _vy
       (sys::poke _vy (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int8 _id
     (setq _id (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> _id 127) (setq _id (- _id 256)))
   ;; float64 _x
     (setq _x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _y
     (setq _y (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _vx
     (setq _vx (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _vy
     (setq _vy (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get cbf_simulation::state_msg :md5sum-) "cc3231566688c318ac8a6b339b1693c0")
(setf (get cbf_simulation::state_msg :datatype-) "cbf_simulation/state_msg")
(setf (get cbf_simulation::state_msg :definition-)
      "int8 id 
float64 x
float64 y
float64 vx
float64 vy
")



(provide :cbf_simulation/state_msg "cc3231566688c318ac8a6b339b1693c0")


