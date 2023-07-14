/**
 * Ardity (Serial Communication for Arduino + Unity)
 * Author: Daniel Wilches <dwilches@gmail.com>
 *
 * This work is released under the Creative Commons Attributions license.
 * https://creativecommons.org/licenses/by/2.0/
 */

using UnityEngine;
using System.Collections;
using System.IO.Ports;

/**
 * Sample for reading using polling by yourself, and writing too.
 */
public class SampleUserPolling_ReadWrite : MonoBehaviour
{
    public SerialController serialController;
    public GameObject cube;
    private SerialPort serialPort;

    // Initialization
    void Start()
    {
        serialController = GameObject.Find("SerialController").GetComponent<SerialController>();

        Debug.Log("Press A or Z to execute some actions");
    }

    // Executed each frame
    void Update()
    {
        //---------------------------------------------------------------------
        // Send data
        //---------------------------------------------------------------------

        // If you press one of these keys send it to the serial device. A
        // sample serial device that accepts this input is given in the README.


        if (Input.GetKeyDown(KeyCode.A))
        {
            Debug.Log("Sending A");
            serialController.SendSerialMessage("A");
        }

        if (Input.GetKeyDown(KeyCode.Z))
        {
            Debug.Log("Sending Z");
            serialController.SendSerialMessage("Z");
        }


        //---------------------------------------------------------------------
        // Receive data
        //---------------------------------------------------------------------

        string message = serialController.ReadSerialMessage();

        if (message == null)
            return;

        // Check if the message is plain data or a connect/disconnect event.
        if (ReferenceEquals(message, SerialController.SERIAL_DEVICE_CONNECTED))
            Debug.Log("Connection established");
        else if (ReferenceEquals(message, SerialController.SERIAL_DEVICE_DISCONNECTED))
            Debug.Log("Connection attempt failed or disconnection detected");
        else
        {
            if (message.StartsWith("UnityData:"))
            {
                string[] values = message.Substring(10).Split(',');
                if (values.Length >= 7)
                {
                    int x, y, z;
                    float ax, ay, az, R;
                    
                    if (int.TryParse(values[0], out x) &&
                        int.TryParse(values[1], out y) &&
                        int.TryParse(values[2], out z) &&
                        float.TryParse(values[3], out ax) &&
                        float.TryParse(values[4], out ay) &&
                        float.TryParse(values[5], out az) &&
                        float.TryParse(values[6], out R))
                    {
                        // 将坐标值应用于Cube的位置
                        cube.transform.position = new Vector3(x, y, z);
                    
                        if (R < 1020)
                        {
                            cube.GetComponent<MeshRenderer>().material.SetColor("Color_", Color.red);
                        }
                        else cube.GetComponent<MeshRenderer>().material.SetColor("Color_", Color.yellow); ;                    
                    }
                }

                Debug.Log("Message arrived: " + message);
            }
        }
    }
}