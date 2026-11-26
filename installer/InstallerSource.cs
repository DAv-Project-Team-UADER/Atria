// Copyright (C) 2026 El Equipo del Proyecto Atria
// Universidad Autónoma de Entre Ríos (UADER FCYT)
// Instalador Autónomo de ATRIA para FreeCAD

using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.IO.Compression;
using System.Reflection;
using System.Runtime.InteropServices;
using System.Text;
using System.Windows.Forms;
using Microsoft.Win32;

namespace AtriaInstaller
{
    public class InstallerForm : Form
    {
        private Panel pnlHeader;
        private Label lblHeaderTitle;
        private Label lblHeaderSub;
        private PictureBox picLogo;

        private GroupBox grpFreeCAD;
        private Label lblFreeCADStatus;
        private LinkLabel lnkFreeCADDownload;

        private GroupBox grpDestination;
        private TextBox txtDestination;
        private Button btnBrowse;

        private GroupBox grpOptions;
        private CheckBox chkDesktopShortcut;
        private CheckBox chkStartMenuShortcut;
        private CheckBox chkLinkAllVersions;
        private CheckBox chkLaunchAfter;

        private ProgressBar prgProgress;
        private Label lblStatus;
        private Label lblDetails;

        private Panel pnlBottom;
        private Button btnInstall;
        private Button btnCancel;

        private string detectedFreeCadExe = null;
        private string defaultModDir = null;
        private BackgroundWorker worker;
        private bool installCompleted = false;

        public InstallerForm()
        {
            InitializeComponent();
            DetectEnvironment();
        }

        private void InitializeComponent()
        {
            this.Text = "Instalador de ATRIA — Asistente de Voz para FreeCAD";
            this.Size = new Size(650, 520);
            this.StartPosition = FormStartPosition.CenterScreen;
            this.FormBorderStyle = FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.Font = new Font("Segoe UI", 9F, FontStyle.Regular, GraphicsUnit.Point);
            this.BackColor = Color.FromArgb(246, 248, 250);

            // Intentar cargar icono embebido
            try {
                this.Icon = Icon.ExtractAssociatedIcon(Assembly.GetExecutingAssembly().Location);
            } catch {}

            // Header Panel
            pnlHeader = new Panel();
            pnlHeader.Dock = DockStyle.Top;
            pnlHeader.Height = 72;
            pnlHeader.BackColor = Color.FromArgb(15, 38, 64);

            lblHeaderTitle = new Label();
            lblHeaderTitle.Text = "ATRIA — Asistente de Voz para FreeCAD";
            lblHeaderTitle.Font = new Font("Segoe UI", 12F, FontStyle.Bold);
            lblHeaderTitle.ForeColor = Color.White;
            lblHeaderTitle.Location = new Point(20, 14);
            lblHeaderTitle.AutoSize = true;

            lblHeaderSub = new Label();
            lblHeaderSub.Text = "Universidad Autónoma de Entre Ríos • FCyT • Concepción del Uruguay";
            lblHeaderSub.Font = new Font("Segoe UI", 8.5F, FontStyle.Regular);
            lblHeaderSub.ForeColor = Color.FromArgb(144, 224, 239);
            lblHeaderSub.Location = new Point(21, 40);
            lblHeaderSub.AutoSize = true;

            pnlHeader.Controls.Add(lblHeaderTitle);
            pnlHeader.Controls.Add(lblHeaderSub);

            // Group FreeCAD Detection
            grpFreeCAD = new GroupBox();
            grpFreeCAD.Text = " 1. Estado de FreeCAD ";
            grpFreeCAD.Location = new Point(20, 84);
            grpFreeCAD.Size = new Size(595, 62);

            lblFreeCADStatus = new Label();
            lblFreeCADStatus.Location = new Point(15, 24);
            lblFreeCADStatus.Size = new Size(420, 26);
            lblFreeCADStatus.Text = "Buscando FreeCAD en el equipo...";

            lnkFreeCADDownload = new LinkLabel();
            lnkFreeCADDownload.Text = "Descargar FreeCAD (Sitio Oficial)";
            lnkFreeCADDownload.Location = new Point(435, 24);
            lnkFreeCADDownload.AutoSize = true;
            lnkFreeCADDownload.Visible = false;
            lnkFreeCADDownload.LinkClicked += (s, e) => {
                try { Process.Start("https://www.freecad.org/downloads.php"); } catch {}
            };

            grpFreeCAD.Controls.Add(lblFreeCADStatus);
            grpFreeCAD.Controls.Add(lnkFreeCADDownload);

            // Group Destination
            grpDestination = new GroupBox();
            grpDestination.Text = " 2. Carpeta de Instalación de la Extensión (Workbench) ";
            grpDestination.Location = new Point(20, 154);
            grpDestination.Size = new Size(595, 65);

            txtDestination = new TextBox();
            txtDestination.Location = new Point(15, 26);
            txtDestination.Size = new Size(475, 25);

            btnBrowse = new Button();
            btnBrowse.Text = "Examinar...";
            btnBrowse.Location = new Point(498, 24);
            btnBrowse.Size = new Size(82, 28);
            btnBrowse.Click += BtnBrowse_Click;

            grpDestination.Controls.Add(txtDestination);
            grpDestination.Controls.Add(btnBrowse);

            // Group Options
            grpOptions = new GroupBox();
            grpOptions.Text = " 3. Opciones de Acceso Directo e Integración ";
            grpOptions.Location = new Point(20, 226);
            grpOptions.Size = new Size(595, 95);

            chkDesktopShortcut = new CheckBox();
            chkDesktopShortcut.Text = "Crear acceso directo en el Escritorio ('Iniciar ATRIA con FreeCAD')";
            chkDesktopShortcut.Location = new Point(15, 22);
            chkDesktopShortcut.Size = new Size(560, 22);
            chkDesktopShortcut.Checked = true;

            chkStartMenuShortcut = new CheckBox();
            chkStartMenuShortcut.Text = "Crear acceso en el Menú Inicio (carpeta 'ATRIA')";
            chkStartMenuShortcut.Location = new Point(15, 44);
            chkStartMenuShortcut.Size = new Size(560, 22);
            chkStartMenuShortcut.Checked = true;

            chkLinkAllVersions = new CheckBox();
            chkLinkAllVersions.Text = "Habilitar para todas las versiones detectadas de FreeCAD (v1-1, v1-0, Mod)";
            chkLinkAllVersions.Location = new Point(15, 66);
            chkLinkAllVersions.Size = new Size(560, 22);
            chkLinkAllVersions.Checked = true;

            grpOptions.Controls.Add(chkDesktopShortcut);
            grpOptions.Controls.Add(chkStartMenuShortcut);
            grpOptions.Controls.Add(chkLinkAllVersions);

            // Progress Controls
            lblStatus = new Label();
            lblStatus.Text = "Listo para comenzar la instalación.";
            lblStatus.Location = new Point(20, 330);
            lblStatus.Size = new Size(595, 18);
            lblStatus.Font = new Font("Segoe UI", 9F, FontStyle.Bold);

            prgProgress = new ProgressBar();
            prgProgress.Location = new Point(20, 352);
            prgProgress.Size = new Size(595, 22);
            prgProgress.Minimum = 0;
            prgProgress.Maximum = 100;
            prgProgress.Value = 0;

            lblDetails = new Label();
            lblDetails.Text = "";
            lblDetails.Location = new Point(20, 378);
            lblDetails.Size = new Size(595, 18);
            lblDetails.ForeColor = Color.FromArgb(100, 110, 120);

            // Bottom Panel
            pnlBottom = new Panel();
            pnlBottom.Dock = DockStyle.Bottom;
            pnlBottom.Height = 52;
            pnlBottom.BackColor = Color.FromArgb(235, 238, 242);

            chkLaunchAfter = new CheckBox();
            chkLaunchAfter.Text = "Iniciar FreeCAD con ATRIA al finalizar";
            chkLaunchAfter.Location = new Point(20, 15);
            chkLaunchAfter.Size = new Size(270, 24);
            chkLaunchAfter.Checked = true;

            btnInstall = new Button();
            btnInstall.Text = "Instalar ATRIA";
            btnInstall.Location = new Point(410, 12);
            btnInstall.Size = new Size(115, 30);
            btnInstall.BackColor = Color.FromArgb(0, 120, 215);
            btnInstall.ForeColor = Color.White;
            btnInstall.FlatStyle = FlatStyle.Flat;
            btnInstall.Font = new Font("Segoe UI", 9F, FontStyle.Bold);
            btnInstall.Click += BtnInstall_Click;

            btnCancel = new Button();
            btnCancel.Text = "Cancelar";
            btnCancel.Location = new Point(535, 12);
            btnCancel.Size = new Size(80, 30);
            btnCancel.Click += (s, e) => { this.Close(); };

            pnlBottom.Controls.Add(chkLaunchAfter);
            pnlBottom.Controls.Add(btnInstall);
            pnlBottom.Controls.Add(btnCancel);

            this.Controls.Add(pnlHeader);
            this.Controls.Add(grpFreeCAD);
            this.Controls.Add(grpDestination);
            this.Controls.Add(grpOptions);
            this.Controls.Add(lblStatus);
            this.Controls.Add(prgProgress);
            this.Controls.Add(lblDetails);
            this.Controls.Add(pnlBottom);

            // BackgroundWorker
            worker = new BackgroundWorker();
            worker.WorkerReportsProgress = true;
            worker.DoWork += Worker_DoWork;
            worker.ProgressChanged += Worker_ProgressChanged;
            worker.RunWorkerCompleted += Worker_RunWorkerCompleted;
        }

        private void DetectEnvironment()
        {
            // 1. Detectar FreeCAD exe
            string[] candidates = new string[] {
                @"C:\Program Files\FreeCAD 1.1inreecad.exe",
                @"C:\Program Files\FreeCAD 1.0inreecad.exe",
                @"C:\Program Files\FreeCAD 0.21inreecad.exe",
                @"C:\Program Files\FreeCADinreecad.exe",
                Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), @"Programs\FreeCAD 1.1inreecad.exe"),
                Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), @"Programs\FreeCAD 1.0inreecad.exe")
            };

            foreach (string path in candidates)
            {
                if (File.Exists(path))
                {
                    detectedFreeCadExe = path;
                    break;
                }
            }

            if (detectedFreeCadExe != null)
            {
                string ver = "FreeCAD";
                if (detectedFreeCadExe.Contains("1.1")) ver = "FreeCAD 1.1";
                else if (detectedFreeCadExe.Contains("1.0")) ver = "FreeCAD 1.0";
                else if (detectedFreeCadExe.Contains("0.21")) ver = "FreeCAD 0.21";

                lblFreeCADStatus.Text = string.Format("✓ {0} detectado correctamente en:\n  {1}", ver, detectedFreeCadExe);
                lblFreeCADStatus.ForeColor = Color.FromArgb(16, 124, 65);
                lnkFreeCADDownload.Visible = false;
            }
            else
            {
                lblFreeCADStatus.Text = "⚠ No se detectó FreeCAD instalado en las rutas estándar.\nPuedes instalar ATRIA ahora y luego instalar FreeCAD.";
                lblFreeCADStatus.ForeColor = Color.FromArgb(180, 80, 0);
                lnkFreeCADDownload.Visible = true;
            }

            // 2. Detectar Carpeta Mod
            string appData = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
            string modernV11 = Path.Combine(appData, @"FreeCAD1-1\Mod");
            string modernV10 = Path.Combine(appData, @"FreeCAD1-0\Mod");
            string classic = Path.Combine(appData, @"FreeCAD\Mod");

            if (detectedFreeCadExe != null && detectedFreeCadExe.Contains("1.1"))
                defaultModDir = Path.Combine(modernV11, "Atria");
            else if (detectedFreeCadExe != null && detectedFreeCadExe.Contains("1.0"))
                defaultModDir = Path.Combine(modernV10, "Atria");
            else if (Directory.Exists(modernV11))
                defaultModDir = Path.Combine(modernV11, "Atria");
            else if (Directory.Exists(modernV10))
                defaultModDir = Path.Combine(modernV10, "Atria");
            else
                defaultModDir = Path.Combine(classic, "Atria");

            txtDestination.Text = defaultModDir;
        }

        private void BtnBrowse_Click(object sender, EventArgs e)
        {
            using (FolderBrowserDialog fbd = new FolderBrowserDialog())
            {
                fbd.Description = "Selecciona la carpeta donde deseas instalar ATRIA:";
                fbd.SelectedPath = Path.GetDirectoryName(txtDestination.Text);
                if (fbd.ShowDialog() == DialogResult.OK)
                {
                    string sel = fbd.SelectedPath;
                    if (!sel.EndsWith("Atria", StringComparison.OrdinalIgnoreCase))
                    {
                        sel = Path.Combine(sel, "Atria");
                    }
                    txtDestination.Text = sel;
                }
            }
        }

        private void BtnInstall_Click(object sender, EventArgs e)
        {
            if (installCompleted)
            {
                if (chkLaunchAfter.Checked)
                {
                    LaunchAtria();
                }
                this.Close();
                return;
            }

            // Iniciar instalación
            btnInstall.Enabled = false;
            btnBrowse.Enabled = false;
            txtDestination.Enabled = false;
            grpOptions.Enabled = false;
            btnCancel.Text = "Cerrar";

            lblStatus.Text = "Iniciando descompresión e instalación de ATRIA...";
            prgProgress.Value = 0;

            InstallParams ip = new InstallParams();
            ip.TargetDir = txtDestination.Text.Trim();
            ip.CreateDesktopShortcut = chkDesktopShortcut.Checked;
            ip.CreateStartMenuShortcut = chkStartMenuShortcut.Checked;
            ip.LinkAllVersions = chkLinkAllVersions.Checked;
            ip.FreeCadExe = detectedFreeCadExe;

            worker.RunWorkerAsync(ip);
        }

        private class InstallParams
        {
            public string TargetDir;
            public bool CreateDesktopShortcut;
            public bool CreateStartMenuShortcut;
            public bool LinkAllVersions;
            public string FreeCadExe;
        }

        private void Worker_DoWork(object sender, DoWorkEventArgs e)
        {
            InstallParams ip = (InstallParams)e.Argument;
            string targetDir = ip.TargetDir;

            Directory.CreateDirectory(targetDir);

            // Obtener recurso embebido
            Assembly asm = Assembly.GetExecutingAssembly();
            using (Stream stream = asm.GetManifestResourceStream("Payload"))
            {
                if (stream == null)
                {
                    throw new InvalidOperationException("No se encontró el paquete de archivos embebido (Payload) en el instalador.");
                }

                using (ZipArchive archive = new ZipArchive(stream, ZipArchiveMode.Read))
                {
                    int total = archive.Entries.Count;
                    int count = 0;

                    foreach (ZipArchiveEntry entry in archive.Entries)
                    {
                        string outPath = Path.Combine(targetDir, entry.FullName.Replace('/', Path.DirectorySeparatorChar));

                        if (string.IsNullOrEmpty(entry.Name))
                        {
                            // Es un directorio
                            Directory.CreateDirectory(outPath);
                        }
                        else
                        {
                            Directory.CreateDirectory(Path.GetDirectoryName(outPath));
                            entry.ExtractToFile(outPath, true);
                        }

                        count++;
                        int pct = (int)((count * 85.0) / total);
                        worker.ReportProgress(pct, "Extrayendo: " + entry.Name);
                    }
                }
            }

            worker.ReportProgress(88, "Configurando scripts y lanzadores de ATRIA...");

            // Guardar icono institucional atria.ico en destino
            string icoPath = Path.Combine(targetDir, "atria.ico");
            try
            {
                using (Stream icoStream = asm.GetManifestResourceStream("Icon"))
                {
                    if (icoStream != null)
                    {
                        using (FileStream fs = new FileStream(icoPath, FileMode.Create, FileAccess.Write))
                        {
                            icoStream.CopyTo(fs);
                        }
                    }
                }
            }
            catch {}

            // Crear lanzador silencioso VBS
            string vbsPath = Path.Combine(targetDir, "iniciar_atria_silencioso.vbs");
            string vbsContent = "Set WshShell = CreateObject(\"WScript.Shell\")\r\n" +
                                "Dim scriptDir\r\n" +
                                "scriptDir = CreateObject(\"Scripting.FileSystemObject\").GetParentFolderName(WScript.ScriptFullName)\r\n" +
                                "WshShell.Run Chr(34) & scriptDir & \"\\iniciar_atria.bat\" & Chr(34), 0, False\r\n";
            File.WriteAllText(vbsPath, vbsContent, Encoding.Default);

            // Crear desinstalador .bat
            string uninstallerBat = Path.Combine(targetDir, "desinstalar_atria.bat");
            string uninstallerContent = "@echo off\r\n" +
                                        "title Desinstalador de ATRIA\r\n" +
                                        "echo ====================================================\r\n" +
                                        "echo           Desinstalador de ATRIA (FreeCAD)\r\n" +
                                        "echo ====================================================\r\n" +
                                        "echo.\r\n" +
                                        "set /p CONFIRM=Esta seguro de que desea desinstalar ATRIA? (S/N): \r\n" +
                                        "if /i \"%CONFIRM%\" NEQ \"S\" (echo Operacion cancelada.& pause & exit /b 0)\r\n" +
                                        "echo Removiendo accesos directos...\r\n" +
                                        "del \"%USERPROFILE%\\Desktop\\Iniciar ATRIA con FreeCAD.lnk\" 2>nul\r\n" +
                                        "del \"%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\ATRIA\\*.*\" 2>nul\r\n" +
                                        "rmdir \"%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\ATRIA\" 2>nul\r\n" +
                                        "reg delete \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\ATRIA\" /f >nul 2>nul\r\n" +
                                        "echo Eliminando archivos de ATRIA...\r\n" +
                                        "cd \"..\"\r\n" +
                                        "rmdir /s /q \"" + targetDir + "\" 2>nul\r\n" +
                                        "echo.\r\n" +
                                        "echo ATRIA ha sido desinstalado correctamente de su equipo.\r\n" +
                                        "pause\r\n";
            File.WriteAllText(uninstallerBat, uninstallerContent, Encoding.Default);

            worker.ReportProgress(92, "Creando enlaces en directorios de FreeCAD...");

            // Enlazar a otras versiones de FreeCAD si se solicitó
            if (ip.LinkAllVersions)
            {
                string appData = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
                string[] otherModDirs = new string[] {
                    Path.Combine(appData, @"FreeCAD\Mod"),
                    Path.Combine(appData, @"FreeCAD1-1\Mod"),
                    Path.Combine(appData, @"FreeCAD1-0\Mod")
                };

                foreach (string mdir in otherModDirs)
                {
                    try
                    {
                        string linkTarget = Path.Combine(mdir, "Atria");
                        if (!linkTarget.Equals(targetDir, StringComparison.OrdinalIgnoreCase))
                        {
                            Directory.CreateDirectory(mdir);
                            if (!Directory.Exists(linkTarget))
                            {
                                // Crear Junction de Windows usando cmd
                                ProcessStartInfo psi = new ProcessStartInfo("cmd.exe", string.Format("/c mklink /J \"{0}\" \"{1}\"", linkTarget, targetDir));
                                psi.CreateNoWindow = true;
                                psi.UseShellExecute = false;
                                Process p = Process.Start(psi);
                                p.WaitForExit(3000);
                            }
                        }
                    }
                    catch {}
                }
            }

            worker.ReportProgress(95, "Creando accesos directos...");

            // Crear accesos directos
            string batPath = Path.Combine(targetDir, "iniciar_atria.bat");
            string iconTarget = File.Exists(icoPath) ? icoPath : "";

            if (ip.CreateDesktopShortcut)
            {
                string desktop = Environment.GetFolderPath(Environment.SpecialFolder.Desktop);
                string lnk = Path.Combine(desktop, "Iniciar ATRIA con FreeCAD.lnk");
                CreateShortcut(lnk, "wscript.exe", string.Format("\"{0}\"", vbsPath), targetDir, iconTarget, "Iniciar FreeCAD con el Asistente de Voz ATRIA");
            }

            if (ip.CreateStartMenuShortcut)
            {
                string startMenu = Environment.GetFolderPath(Environment.SpecialFolder.Programs);
                string atriaFolder = Path.Combine(startMenu, "ATRIA");
                Directory.CreateDirectory(atriaFolder);

                string lnkMain = Path.Combine(atriaFolder, "Iniciar ATRIA (FreeCAD).lnk");
                CreateShortcut(lnkMain, "wscript.exe", string.Format("\"{0}\"", vbsPath), targetDir, iconTarget, "Iniciar FreeCAD con ATRIA");

                string lnkUninst = Path.Combine(atriaFolder, "Desinstalar ATRIA.lnk");
                CreateShortcut(lnkUninst, "cmd.exe", string.Format("/c \"{0}\"", uninstallerBat), targetDir, "", "Desinstalar ATRIA");
            }

            // Registro en Windows para Agregar/Quitar programas
            try
            {
                using (RegistryKey key = Registry.CurrentUser.CreateSubKey(@"Software\Microsoft\Windows\CurrentVersion\Uninstall\ATRIA"))
                {
                    if (key != null)
                    {
                        key.SetValue("DisplayName", "ATRIA — Asistente de Voz para FreeCAD");
                        key.SetValue("DisplayVersion", "1.0.0");
                        key.SetValue("Publisher", "Universidad Autónoma de Entre Ríos (UADER FCyT)");
                        key.SetValue("InstallLocation", targetDir);
                        key.SetValue("UninstallString", string.Format("cmd.exe /c \"{0}\"", uninstallerBat));
                        if (File.Exists(icoPath)) key.SetValue("DisplayIcon", icoPath);
                    }
                }
            }
            catch {}

            worker.ReportProgress(100, "¡Instalación completada!");
        }

        private void Worker_ProgressChanged(object sender, ProgressChangedEventArgs e)
        {
            prgProgress.Value = Math.Min(100, Math.Max(0, e.ProgressPercentage));
            lblStatus.Text = string.Format("Instalando ATRIA... ({0}%)", prgProgress.Value);
            lblDetails.Text = e.UserState != null ? e.UserState.ToString() : "";
        }

        private void Worker_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
        {
            if (e.Error != null)
            {
                lblStatus.Text = "Error durante la instalación.";
                lblStatus.ForeColor = Color.Red;
                lblDetails.Text = e.Error.Message;
                MessageBox.Show(
                    "Ocurrió un error al instalar ATRIA:\n" + e.Error.Message,
                    "Error de instalación",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error
                );
                btnInstall.Enabled = true;
                btnInstall.Text = "Reintentar";
            }
            else
            {
                installCompleted = true;
                lblStatus.Text = "✓ ¡ATRIA ha sido instalado exitosamente!";
                lblStatus.ForeColor = Color.FromArgb(16, 124, 65);
                lblDetails.Text = "La extensión ya está disponible y vinculada a FreeCAD.";
                prgProgress.Value = 100;

                btnInstall.Enabled = true;
                btnInstall.Text = "Finalizar";
                btnCancel.Visible = false;

                MessageBox.Show(
                    "¡ATRIA se ha instalado con éxito!\n\n" +
                    "Puedes iniciarlo desde el acceso directo en tu Escritorio o seleccionando el Workbench ATRIA dentro de FreeCAD.",
                    "Instalación Exitosa",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Information
                );
            }
        }

        private void LaunchAtria()
        {
            try
            {
                string vbs = Path.Combine(txtDestination.Text, "iniciar_atria_silencioso.vbs");
                if (File.Exists(vbs))
                {
                    ProcessStartInfo psi = new ProcessStartInfo("wscript.exe", string.Format("\"{0}\"", vbs));
                    psi.WorkingDirectory = txtDestination.Text;
                    Process.Start(psi);
                    return;
                }

                string bat = Path.Combine(txtDestination.Text, "iniciar_atria.bat");
                if (File.Exists(bat))
                {
                    ProcessStartInfo psi = new ProcessStartInfo(bat);
                    psi.WorkingDirectory = txtDestination.Text;
                    Process.Start(psi);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("No se pudo iniciar automáticamente: " + ex.Message);
            }
        }

        private static void CreateShortcut(string shortcutPath, string targetPath, string arguments, string workingDirectory, string iconLocation, string description)
        {
            try
            {
                Type shellType = Type.GetTypeFromProgID("WScript.Shell");
                if (shellType == null) return;
                object shell = Activator.CreateInstance(shellType);
                object shortcut = shellType.InvokeMember("CreateShortcut", BindingFlags.InvokeMethod, null, shell, new object[] { shortcutPath });
                Type scType = shortcut.GetType();
                scType.InvokeMember("TargetPath", BindingFlags.SetProperty, null, shortcut, new object[] { targetPath });
                if (!string.IsNullOrEmpty(arguments)) scType.InvokeMember("Arguments", BindingFlags.SetProperty, null, shortcut, new object[] { arguments });
                if (!string.IsNullOrEmpty(workingDirectory)) scType.InvokeMember("WorkingDirectory", BindingFlags.SetProperty, null, shortcut, new object[] { workingDirectory });
                if (!string.IsNullOrEmpty(iconLocation) && File.Exists(iconLocation)) scType.InvokeMember("IconLocation", BindingFlags.SetProperty, null, shortcut, new object[] { iconLocation + ",0" });
                if (!string.IsNullOrEmpty(description)) scType.InvokeMember("Description", BindingFlags.SetProperty, null, shortcut, new object[] { description });
                scType.InvokeMember("Save", BindingFlags.InvokeMethod, null, shortcut, null);
            }
            catch {}
        }

        [STAThread]
        static void Main(string[] args)
        {
            // Soporte modo silencioso: /S o /silent
            bool silent = false;
            string customTarget = null;
            foreach (string arg in args)
            {
                if (arg.Equals("/S", StringComparison.OrdinalIgnoreCase) || arg.Equals("/silent", StringComparison.OrdinalIgnoreCase))
                {
                    silent = true;
                }
                else if (arg.StartsWith("/D=", StringComparison.OrdinalIgnoreCase) || arg.StartsWith("/target=", StringComparison.OrdinalIgnoreCase))
                {
                    customTarget = arg.Substring(arg.IndexOf('=') + 1).Trim('"', ' ');
                }
            }

            if (silent)
            {
                try
                {
                    string target = customTarget;
                    if (string.IsNullOrEmpty(target))
                    {
                        string appData = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
                        target = Path.Combine(appData, @"FreeCAD\Mod\Atria");
                    }
                    Directory.CreateDirectory(target);
                    Assembly asm = Assembly.GetExecutingAssembly();
                    using (Stream stream = asm.GetManifestResourceStream("Payload"))
                    using (ZipArchive archive = new ZipArchive(stream, ZipArchiveMode.Read))
                    {
                        foreach (ZipArchiveEntry entry in archive.Entries)
                        {
                            string outPath = Path.Combine(target, entry.FullName.Replace('/', Path.DirectorySeparatorChar));
                            if (string.IsNullOrEmpty(entry.Name)) Directory.CreateDirectory(outPath);
                            else { Directory.CreateDirectory(Path.GetDirectoryName(outPath)); entry.ExtractToFile(outPath, true); }
                        }
                    }
                    Environment.Exit(0);
                }
                catch
                {
                    Environment.Exit(1);
                }
                return;
            }

            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new InstallerForm());
        }
    }
}
