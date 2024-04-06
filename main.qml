import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Window

ApplicationWindow {
    width: 640
    height: 480
    visible: true
    title: qsTr("Speech Recognizer")
    color: "lightblue"


    Rectangle {
           id: rectangle
           anchors.centerIn: parent


           ColumnLayout {

               anchors.centerIn: parent
               spacing: 10



               Button {
                     id: start
                     text: "Start..."
                     implicitWidth: 100
                     implicitHeight: 50
                     Layout.alignment: Qt.AlignHCenter

                     background: Rectangle {
                         color: "#007bff"
                         radius: 5
                     }

                     font.bold: true
                     //color: "white"

                     onClicked: {
                        command.text = "Enter command !"
                        //Qt.binding(function() { return; })
                        controller.command()
                     }

                }



               Label {
                   id: command
                   text: "Command ..."
                   Layout.alignment: Qt.AlignHCenter


               }




                Connections {
                        target: controller

                        function onUpdateLabel(newText) {
                            console.log("updating element text ...")
                            command.text = newText

                        }
                }





            }
    }
}
