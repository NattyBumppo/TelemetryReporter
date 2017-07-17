Telemetry Reporter
===================

## Summary

This is a tool to easily build interactive reports for telemetry captured during engineering tests and missions. The tool accepts a number of different types of vehicle/system telemetry, including:

- Timestamped channel values
- Event logs
- State transitions
- Position/orientation updates
- Fault detection thresholds
- Images

When this telemetry data is supplied as input, the Telemetry Reporter tool will generate an interactive set of visualizations which make it possible to easily see the system's changing state over time, and to examine data looking for anomalies. Generated visualizations are customizable and can be uploaded to a server as web content and served out as interactive reports, making them easily sharable with other team members.

## File Structure

Input files must be given specific names in order to be automatically ingested by the Telemetry Reporter tool. A sample file structure, with comments, is below:

```
project
│
│   generate_report.py (Run this script to generate an interactive report)
│
└───input
│   │   events.csv (Timestamped event list)
│   │   channel_data.csv (Timestamped channel values)
│   │   channel_metadata.json (Channel subsystems, units, etc.)
│   │   fault_thresholds.json (Defined safety thresholds for each telemetry channel)
│   │   state_transitions.csv (Timestamped entrance/exits for named states)
│   │
│   └───images
│   │   │   image_metadata.csv (Timestamps for each image file)
│   │   │   mainCam001.png (Single image data product--filename is arbitrary)
│   │   │   mainCam002.png
│   │   │   sideCamL000.png
│   │   │   sideCamL001.png
│   │   └   ...
│   │
│   └───poses
│   │   │   main_poses.csv (Timestamped positions/orientations for object)
│   │   |   staticObjects.json (Positions/orientations/models to use for objects that never move)
|   |   |   main_model.obj (3D model of main vehicle/system for rendering position/orientation over time)
|   |   |   model_001.obj (3D model for object that never moves--filename is arbitrary)
|   |   |   model_002.obj
│   │   └   ...
│   │
│   └───customization
│       │   logo.png (Team/project logo)
│       │   customization_metadata.json (Name of team, name of test, color scheme, visualization options, etc.)
|       └   ...
|
└───output (Contains generated report after running generate_report.py)
    │   index.html (Main page of report)
    │
    └───content (Content needed to display report)
```
