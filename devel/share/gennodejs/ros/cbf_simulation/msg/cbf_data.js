// Auto-generated. Do not edit!

// (in-package cbf_simulation.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class cbf_data {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.stamp = null;
      this.px = null;
      this.py = null;
      this.vx = null;
      this.vy = null;
      this.ux_nom = null;
      this.uy_nom = null;
      this.ux_safe = null;
      this.uy_safe = null;
    }
    else {
      if (initObj.hasOwnProperty('stamp')) {
        this.stamp = initObj.stamp
      }
      else {
        this.stamp = {secs: 0, nsecs: 0};
      }
      if (initObj.hasOwnProperty('px')) {
        this.px = initObj.px
      }
      else {
        this.px = 0.0;
      }
      if (initObj.hasOwnProperty('py')) {
        this.py = initObj.py
      }
      else {
        this.py = 0.0;
      }
      if (initObj.hasOwnProperty('vx')) {
        this.vx = initObj.vx
      }
      else {
        this.vx = 0.0;
      }
      if (initObj.hasOwnProperty('vy')) {
        this.vy = initObj.vy
      }
      else {
        this.vy = 0.0;
      }
      if (initObj.hasOwnProperty('ux_nom')) {
        this.ux_nom = initObj.ux_nom
      }
      else {
        this.ux_nom = 0.0;
      }
      if (initObj.hasOwnProperty('uy_nom')) {
        this.uy_nom = initObj.uy_nom
      }
      else {
        this.uy_nom = 0.0;
      }
      if (initObj.hasOwnProperty('ux_safe')) {
        this.ux_safe = initObj.ux_safe
      }
      else {
        this.ux_safe = 0.0;
      }
      if (initObj.hasOwnProperty('uy_safe')) {
        this.uy_safe = initObj.uy_safe
      }
      else {
        this.uy_safe = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type cbf_data
    // Serialize message field [stamp]
    bufferOffset = _serializer.time(obj.stamp, buffer, bufferOffset);
    // Serialize message field [px]
    bufferOffset = _serializer.float64(obj.px, buffer, bufferOffset);
    // Serialize message field [py]
    bufferOffset = _serializer.float64(obj.py, buffer, bufferOffset);
    // Serialize message field [vx]
    bufferOffset = _serializer.float64(obj.vx, buffer, bufferOffset);
    // Serialize message field [vy]
    bufferOffset = _serializer.float64(obj.vy, buffer, bufferOffset);
    // Serialize message field [ux_nom]
    bufferOffset = _serializer.float64(obj.ux_nom, buffer, bufferOffset);
    // Serialize message field [uy_nom]
    bufferOffset = _serializer.float64(obj.uy_nom, buffer, bufferOffset);
    // Serialize message field [ux_safe]
    bufferOffset = _serializer.float64(obj.ux_safe, buffer, bufferOffset);
    // Serialize message field [uy_safe]
    bufferOffset = _serializer.float64(obj.uy_safe, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type cbf_data
    let len;
    let data = new cbf_data(null);
    // Deserialize message field [stamp]
    data.stamp = _deserializer.time(buffer, bufferOffset);
    // Deserialize message field [px]
    data.px = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [py]
    data.py = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [vx]
    data.vx = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [vy]
    data.vy = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [ux_nom]
    data.ux_nom = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [uy_nom]
    data.uy_nom = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [ux_safe]
    data.ux_safe = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [uy_safe]
    data.uy_safe = _deserializer.float64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 72;
  }

  static datatype() {
    // Returns string type for a message object
    return 'cbf_simulation/cbf_data';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'c9f6db06237f3b61c11f2d3385758187';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    time stamp
    float64 px
    float64 py
    float64 vx
    float64 vy
    float64 ux_nom
    float64 uy_nom
    float64 ux_safe
    float64 uy_safe
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new cbf_data(null);
    if (msg.stamp !== undefined) {
      resolved.stamp = msg.stamp;
    }
    else {
      resolved.stamp = {secs: 0, nsecs: 0}
    }

    if (msg.px !== undefined) {
      resolved.px = msg.px;
    }
    else {
      resolved.px = 0.0
    }

    if (msg.py !== undefined) {
      resolved.py = msg.py;
    }
    else {
      resolved.py = 0.0
    }

    if (msg.vx !== undefined) {
      resolved.vx = msg.vx;
    }
    else {
      resolved.vx = 0.0
    }

    if (msg.vy !== undefined) {
      resolved.vy = msg.vy;
    }
    else {
      resolved.vy = 0.0
    }

    if (msg.ux_nom !== undefined) {
      resolved.ux_nom = msg.ux_nom;
    }
    else {
      resolved.ux_nom = 0.0
    }

    if (msg.uy_nom !== undefined) {
      resolved.uy_nom = msg.uy_nom;
    }
    else {
      resolved.uy_nom = 0.0
    }

    if (msg.ux_safe !== undefined) {
      resolved.ux_safe = msg.ux_safe;
    }
    else {
      resolved.ux_safe = 0.0
    }

    if (msg.uy_safe !== undefined) {
      resolved.uy_safe = msg.uy_safe;
    }
    else {
      resolved.uy_safe = 0.0
    }

    return resolved;
    }
};

module.exports = cbf_data;
