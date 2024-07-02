
(cl:in-package :asdf)

(defsystem "cbf_simulation-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "cbf_data" :depends-on ("_package_cbf_data"))
    (:file "_package_cbf_data" :depends-on ("_package"))
    (:file "state_msg" :depends-on ("_package_state_msg"))
    (:file "_package_state_msg" :depends-on ("_package"))
  ))