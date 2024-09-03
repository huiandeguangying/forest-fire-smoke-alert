# forest-fire-smoke-alert
  该系统在本地计算机上使用 YOLOv5 模型进行烟雾检测。YOLOv5 是一种高效的目标检测模型，能够在复杂的场景中快速识别火灾烟雾。该模型部署在高性能硬件上，以确保实时响应和高精度的检测效果，在使用时对获取的图片可以进行推理，以检测火情。部署在树莓派上部署了 YOLOv5-Lite 版本，以实现低功耗设备上的烟雾检测。YOLOv5-Lite 是 YOLOv5 的简化版本，专为资源受限的设备设计，尽管计算资源有限，它仍能提供可靠的检测性能。树莓派设备负责监控远程或野外的森林区域，上位机可获得相应检测结果。
  
  运行cs.py即可启用上位机。
  ![image](https://github.com/user-attachments/assets/4458e7d8-3d6a-4de3-9fde-a45af0aba4a5)  
  
  选择好图片存放路径以及图片位置，点击推理，即可使用配置好的yolov5s算法推理森林火灾发生时的烟雾，较为清晰。
  ![image0](https://github.com/user-attachments/assets/bf6be8e6-6f71-4a32-ad08-03b3d8b6d03d)  

  其中打开摄像可以开启安装在树莓派4b上的摄像头，实现实时推理，推理帧数稳定在2~3fps之间。
