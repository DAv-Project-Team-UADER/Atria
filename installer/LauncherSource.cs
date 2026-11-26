using System;
using System.Diagnostics;
using System.IO;
using System.Windows.Forms;

class Launcher {
    [STAThread]
    static void Main() {
        try {
            string myDir = AppDomain.CurrentDomain.BaseDirectory.TrimEnd('\\');
            
            // 1. Detectar FreeCAD
            string localApp = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
            string[] candidates = new string[] {
                @"C:\Program Files\FreeCAD 1.1\bin\freecad.exe",
                @"C:\Program Files\FreeCAD 1.0\bin\freecad.exe",
                @"C:\Program Files\FreeCAD 0.21\bin\freecad.exe",
                @"C:\Program Files\FreeCAD\bin\freecad.exe",
                Path.Combine(localApp, @"Programs\FreeCAD 1.1\bin\freecad.exe"),
                Path.Combine(localApp, @"Programs\FreeCAD 1.0\bin\freecad.exe")
            };
            string freeCadExe = null;
            foreach (string p in candidates) {
                if (File.Exists(p)) { freeCadExe = p; break; }
            }
            if (freeCadExe == null) {
                string pathEnv = Environment.GetEnvironmentVariable("PATH") ?? "";
                foreach (string dir in pathEnv.Split(';')) {
                    string test = Path.Combine(dir.Trim(), "freecad.exe");
                    if (File.Exists(test)) { freeCadExe = test; break; }
                }
            }

            if (freeCadExe == null) {
                MessageBox.Show(
                    "No se encontró FreeCAD instalado en las rutas habituales.\n\nPor favor asegúrate de tener instalado FreeCAD 1.0 o 1.1.",
                    "ATRIA - FreeCAD no encontrado",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Warning
                );
                return;
            }

            // 2. Configurar variables de entorno e iniciar FreeCAD
            ProcessStartInfo psi = new ProcessStartInfo(freeCadExe);
            psi.WorkingDirectory = Path.GetDirectoryName(freeCadExe);
            psi.UseShellExecute = false;

            psi.EnvironmentVariables["ATRIA_MOD_ROOT"] = myDir;
            psi.EnvironmentVariables["ATRIA_GUI_FREECAD_ROOT"] = Path.Combine(myDir, "GUIFreeCad");
            psi.EnvironmentVariables["ATRIA_INTERFAZ_ROOT"] = Path.Combine(myDir, "InterfazATRIA");
            string iconsPath = Path.Combine(myDir, @"InterfazATRIA\Icons");
            if (!Directory.Exists(iconsPath)) iconsPath = Path.Combine(myDir, @"GUIFreeCad\ui\Icons");
            psi.EnvironmentVariables["ATRIA_ICONS_ROOT"] = iconsPath;
            psi.EnvironmentVariables["ATRIA_DICTIONARY_ROOT"] = Path.Combine(myDir, "dictionary");
            psi.EnvironmentVariables["ATRIA_MODELS_DIR"] = Path.Combine(myDir, "models");
            psi.EnvironmentVariables["ATRIA_AUTOLOAD_WORKBENCH"] = "1";
            psi.EnvironmentVariables["ATRIA_AUTO_START_VOICE"] = "1";
            psi.EnvironmentVariables["ATRIA_AUTO_PANEL"] = "1";

            Process.Start(psi);
        } catch (Exception ex) {
            MessageBox.Show("Error al iniciar ATRIA:\n\n" + ex.Message, "Error ATRIA", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }
}
