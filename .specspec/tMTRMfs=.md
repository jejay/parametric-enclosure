---
id: tMTRMfs=
type: requirement
parents:
- otMd0TA=
- fstOLa0=
---
# ESP32-S3 with Bluetooth LE and 16 MB of flash

A Seeed XIAO ESP32-S3 Plus runs the device. The phone connects over Bluetooth LE, computes its own GPS distance to the next hiding place and sends only a blink pattern, a clip number or the open command. The recorded messages are MP3 files in the controller's flash and play without any phone once a figure on the grass has woken it.

Firmware and app stay out of scope for now. That the hardware suffices is argued in research/07_firmware_app_feasibility.md and fixed in docs/electronics.md: pin map, power sequence and storage layout.

Live audio from the phone is not possible with this chip. Hints are stored clips.

Origin: agent conclusion.
