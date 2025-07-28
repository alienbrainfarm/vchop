; vchop NSIS Installer Script
; Nullsoft Scriptable Install System (NSIS) installer for vchop

;--------------------------------
; General

; Name and version
!define APPNAME "vchop"
!define VERSION "1.0.0"
!define PUBLISHER "AlienBrainFarm"
!define DESCRIPTION "Advanced video scene detection and splitting tool"

Name "${APPNAME} ${VERSION}"
OutFile "vchop-${VERSION}-setup.exe"
Unicode True

; Default installation directory
InstallDir "$PROGRAMFILES64\${APPNAME}"

; Get installation folder from registry if available
InstallDirRegKey HKCU "Software\${APPNAME}" ""

; Request application privileges
RequestExecutionLevel admin

;--------------------------------
; Interface Settings

!include "MUI2.nsh"

; Icon (if you have one, otherwise comment out)
; !define MUI_ICON "icon.ico"

; Header image (if you have one, otherwise comment out) 
; !define MUI_HEADERIMAGE
; !define MUI_HEADERIMAGE_BITMAP "header.bmp"

; Welcome page image (if you have one, otherwise comment out)
; !define MUI_WELCOMEFINISHPAGE_BITMAP "welcome.bmp"

; Settings
!define MUI_ABORTWARNING

;--------------------------------
; Pages

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

;--------------------------------
; Languages

!insertmacro MUI_LANGUAGE "English"

;--------------------------------
; Version Information

VIProductVersion "1.0.0.0"
VIAddVersionKey "ProductName" "${APPNAME}"
VIAddVersionKey "CompanyName" "${PUBLISHER}" 
VIAddVersionKey "LegalCopyright" "© ${PUBLISHER}"
VIAddVersionKey "FileDescription" "${DESCRIPTION}"
VIAddVersionKey "FileVersion" "${VERSION}"
VIAddVersionKey "ProductVersion" "${VERSION}"

;--------------------------------
; Installer Sections

Section "vchop Application" SecApp
  SectionIn RO  ; Read-only section (always installed)
  
  ; Set output path to installation directory
  SetOutPath $INSTDIR
  
  ; Install executable and required files
  File "dist\vchop.exe"
  
  ; Install additional files if they exist
  File /nonfatal "README.md"
  File /nonfatal "LICENSE"
  
  ; Store installation folder
  WriteRegStr HKCU "Software\${APPNAME}" "" $INSTDIR
  
  ; Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  
  ; Add to Add/Remove Programs
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                   "DisplayName" "${APPNAME} ${VERSION}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                   "UninstallString" "$INSTDIR\Uninstall.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                   "Publisher" "${PUBLISHER}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                   "DisplayVersion" "${VERSION}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                   "DisplayIcon" "$INSTDIR\vchop.exe"
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                     "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                     "NoRepair" 1
  
SectionEnd

Section "Start Menu Shortcuts" SecStartMenu
  ; Create start menu shortcuts
  CreateDirectory "$SMPROGRAMS\${APPNAME}"
  CreateShortcut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\vchop.exe"
  CreateShortcut "$SMPROGRAMS\${APPNAME}\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
SectionEnd

Section "Desktop Shortcut" SecDesktop  
  ; Create desktop shortcut
  CreateShortcut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\vchop.exe"
SectionEnd

;--------------------------------
; Section Descriptions

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SecApp} "The main vchop application (required)"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecStartMenu} "Start menu shortcuts for easy access"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecDesktop} "Desktop shortcut for quick access"
!insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------
; Uninstaller Section

Section "Uninstall"
  ; Remove files
  Delete "$INSTDIR\vchop.exe"
  Delete "$INSTDIR\README.md"
  Delete "$INSTDIR\LICENSE"
  Delete "$INSTDIR\Uninstall.exe"
  
  ; Remove shortcuts
  Delete "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk"
  Delete "$SMPROGRAMS\${APPNAME}\Uninstall.lnk"
  Delete "$DESKTOP\${APPNAME}.lnk"
  
  ; Remove start menu folder
  RMDir "$SMPROGRAMS\${APPNAME}"
  
  ; Remove installation directory if empty
  RMDir "$INSTDIR"
  
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"
  DeleteRegKey HKCU "Software\${APPNAME}"
  
SectionEnd

;--------------------------------
; Functions

Function .onInit
  ; Check for existing installation
  ReadRegStr $R0 HKCU "Software\${APPNAME}" ""
  StrCmp $R0 "" done
  
  MessageBox MB_OKCANCEL|MB_ICONEXCLAMATION \
  "${APPNAME} is already installed. $\n$\nClick `OK` to remove the \
  previous version or `Cancel` to cancel this upgrade." \
  IDOK uninst
  Abort
  
  uninst:
    ClearErrors
    ExecWait '$R0\Uninstall.exe _?=$R0'
    
    IfErrors no_remove_uninstaller done
      Delete $R0\Uninstaller.exe
      RMDir $R0
    no_remove_uninstaller:
    
  done:
  
FunctionEnd