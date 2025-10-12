# Why and for what? 
Fortran its a software used since the late 80s. (Mention some examples of programs, product development or current job positions were fortran is still used). Its a scientific high-level-programming language, 10 to 50 times faster than python as a comparative. ONLY use when the machine or product uses Fortran as a software for interaction and edition or its a MUST for fast numerical iteration as 3D CFD/FEA simulations of specific components or systems.

Installation guide:
1. Go to https://www.msys2.org/ 
2. Download and install and run the .exe
3. After installation look for MSYS2 and open the app
4. In MSYS2 run this line:
    pacman -S mingw-w64-x86_64-gcc-fortran
5. When the terminal ask for something type "Y" and press Enter

After installation add GFortran to the PATH of windows, as you need that windows recognize the command "gfortran"
1. Look for "Environment variables" in Windows
2. Click on "Environment variables"
3. In look for "Path" and click in "Edit"
4. Click on "New" and add:
    C:\msys64\mingw64\bin
5. Click on "Accept"
6. Verify a correct installation, open up PowerShell and type:
    gfortran --version
