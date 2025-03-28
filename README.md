The real-time monitoring system developed in Python and Tkinter. The purpose of this app is to monitor system resources in real time, such as CPU usage, memory usage, disk usage, and processes running on the system. The app is directed toward users that want to monitor system usage performance, identify resource-heavy applications, and end applications. The app updates system stats continuously and displays them using user-friendly progress bars and tables. This app returns and displays all processes which appear in memory, along with their memory/CPU usage, which can be terminated with minimal effort. The app also has a resource hog feature which actively detects processes that are using too much CPU or memory, then highlights them for termination. psutil is a library that is used to collect system statics and can update continuously to provide current and reliable statistics. The Simple System Monitor is user-friendly and easy to navigate, providing real time monitoring and health of system use, and will optimize the way your system operates at home and in practice.

2.Module-Wise Breakdown:

The simulator consists of the following key modules:
2.1 Graphical User Interface Module:
This is responsible for designing and maintaining the GUI through tkinter and ttk. There are functions to create widgets, including:
•	System Metrics Frame (CPU, Memory, and Disk Usage with Progress Bars).
•	Process List (Tree View) (Shows running processes and their CPU and memory usage).
•	Control Buttons (End Process, Refresh, CPU Hogs, Memory Hogs, Exit).
It uses event-driven programming, utilizing root. after () to periodically update the GUI. It calls functions from monitor.py to return system statistics and process information. This component is responsible for organizing the user interface for the application using Tkinter and ttk and establishing a layout of components within the user interface (UI) that will manage the various modelled processes and metrics. The UI contains major components such as a System Metrics Frame that displays the CPU, memory, and disk space being utilized, and recognizes utilization with progress bars, a Process List (Tree View) that will display running processes with CPU and memory percentages honoured, and Control Buttons that performs the actions of killing a process, refreshing the process list, filtering for high resource consuming processes, and exiting the application. The application leverages event-driven programming with root. After () to periodically call and render updated GUI data to the screen so that system data can be received and viewed in the real world. Providing system statistics and process data utilization is achieved through functions called from the System Monitoring Module as there are delimited chances of being interactive and responsive within the user experience.

2.2 System Monitoring Module:
Employs psutil to collect:
•	Percentage of CPU activity.
•	Percentage of memory use.
•	Percentage of disk space being used.
•	Running process list of (PID, Name, CPU %, Memory %).
Employs an independent background thread to continually poll and update system statistics.
Provides routines to:
•	Obtain and sort process data.
•	Find CPU and memory hungry processes.
•	Format statistics for printing.
This module collects and refreshes system performance data in real time with the help of the psutil library. It collects the usage of the CPU, memory, disk, and a list of processes that run on the system. For the processes, the information collected contains the process ID (PID), the name, the amount of CPU usage, and the percentage of memory usage. A separate thread runs in the background and updates and fetches system statistics continuously to ensure that the data is being collected in the background without pausing the GUI process. The module contains methods that return and sort processes, notify the user about processes that are using a large amount of CPU or memory, and formats statistics for easy representation to the user interface. The collected system data will be sent at the appropriate times to the Graphical User Interface Module to display it to the user for monitoring the performance of the machine.

2.3 Process Control Module:
•	Safely kill processes.
•	Provides a method that will confirm ending a selected process by PID.
•	Uses psutil.Process.terminate() to kill processes.
•	Handles any errors when a process cannot be killed.
•	Refreshes the process list with monitor.py following termination.
This module manages the termination of running processes in a safe and efficient manner. There is a function to terminate a selected process by PID; the user must confirm this action before the process can be terminated. This is to prevent the user from accidentally terminating a critical system application. The termination is accomplished using psutil.Process.terminate(), which ensures a safe termination of the selected process. The module has error handling mechanisms in place to handle scenarios where a process cannot be terminated due to insufficient permission or any restrictions set by the operating system. Once a process has been terminated, the module utilizes the System Monitoring Module to refresh the list of processes so that the displayed information is up to date.

3. Functionalities:
The real-time process monitoring system includes several important functions to help users monitor and manage system resources efficiently.

•	Monitor Resource Usage – The system monitors CPU, Memory, and Disk usage in real time and displays the percentage values, using progress bars that change colour based on usage.
•	Process Management – The application retrieves and displays a list of active processes running on the system, along with their Process ID (PID), name, CPU, and Memory usage.
•	Kill Processes – Users can select and kill a process directly from the user interface to eliminate unwanted or unresponsive processes, helping reduce system resource consumption.
•	Highlight CPU and Memory Hogs – The system identifies and highlights processes consuming excessive CPU or Memory resources so users can take appropriate action.
•	Automatic / Manual Update of Resources – The system automatically tracks the list of processes in real time, if users want to manually update the process list, they can click to fetch that information instantaneously.
•	User-Friendly Interface – The user interface is user-friendly and is a simple and structured GUI built with Tkinter, enabling efficient access to system resource consumption and process management.
•	Handling Graceful Exit – The system handles graceful exit by stopping monitoring threads prior to exiting the application.

4. Technology Used:
Programming Languages:
•	Python - chosen for its simplicity and powerful libraries for system monitoring and GUI development.
Libraries and Tools:
•	Tkinter – For building the graphical user interface (GUI).
•	ttk (Themed Tkinter Widgets) – For creating modern UI elements such as progress bars, buttons, and tree views.
•	psutil – To retrieve system resource usage and process details, such as CPU and memory consumption.
•	Threading – For running background tasks, ensuring the GUI remains responsive while monitoring system resources in real-time.
