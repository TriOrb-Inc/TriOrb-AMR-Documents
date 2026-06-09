# Changelog

:::{note}
Per-release details are published on GitHub. This page summarizes the
highlights of the latest release in plain prose; refer to the GitHub
release notes for exact PR / commit lists. Earlier releases remain on
the legacy MkDocs archive
([v1.2.3](../../v1.2.3/TriOrb-AMR-Package/History/),
[v1.2.2](../../v1.2.2/TriOrb-AMR-Package/History/)).
:::

## v1.2.4

Documentation stack switches to Sphinx + rosdoc2 + Furo. English is the
source of truth; the Japanese site is produced from PO translations.
Use the language switcher in the sidebar to swap between Japanese and
English.

Headline functional changes in the `1.2.4.2` release (2026-04-07):

- **Navigation / drive control**: tidied up `stop` / `pause` delay and
  wait-time coordination with `snr_mux`, and reworked how the PICO
  connection timeout is handled. Goal XY judgment is now elliptical
  and idle-state navigation loop input reset is fixed.
- **Manual operation / gamepad**: axis zero-range handling; suppress
  publish during autonomous motion; manual block stop / safe run
  controls; improved deadzone behavior.
- **VSLAM / mapping / camera / MQTT**: restart VSLAM against the last
  loaded map; tracked-landmarks overlay; log preservation on abnormal
  termination. `run_mapping.sh` shows startup progress; camera now
  handles `AutoGainTarget`, scalar parameter parsing, and
  camera-disconnect scenarios; MQTT has improved reconnection
  resilience and startup-time client configuration injection.
- **GUI / platform / diagnostics**: updated `gui/html` and
  `gui/launcher`; fixed topic names when `ROS_PREFIX` is applied;
  beacon DDS priority adjustment. Offline local installer bundle;
  `dead_reckoning` ISAM removal; IMU bypass/verification logging.

Full release notes:
[TriOrb-AMR-Package 1.2.4.2](https://github.com/TriOrb-Inc/TriOrb-AMR-Package/releases/tag/1.2.4.2)

Notable merged PRs: #405 (`dev/std1.2.4` rollup), #397 (PICO timeout
and `snr_mux` wait-time parameterization), #388 (`triorb_gamepad` axis
zero range), #378 (release/std1.2.4 navigation stabilization and Bison
feature landing).

Headline functional changes in the `1.2.4.18` release (2026-06-09):

The `1.2.4.18` release reflects issues and verification results found
during field trials after `1.2.4.2`. It improves stability around
collaboration transport, VSLAM / TagSLAM map operation, temporary
localization loss, compute resources, hardware handshakes, UI / API
behavior, and diagnostic logging.

- Improved behavior so the robot is less likely to move toward a wrong
  position immediately after map switching or temporary localization
  loss.
- Improved pose stability after camera ON / OFF switching.
- Fixed communication loss, reconnection, pause, and resume behavior
  during collaboration transport.
- Faster map file loading and saving.
- Added handshakes for safety sensors, PLC, lifter, and remote-control
  operations.
- Reduced process and communication resource usage to improve resistance
  to resource exhaustion.

Rollup PR:
[TriOrb-AMR-Package #557](https://github.com/TriOrb-Inc/TriOrb-AMR-Package/pull/557)
