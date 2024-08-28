# Importing the vtk library and modules

import vtk
from vtk import *
import vtk

# Taking user input for pressure value
pressure_value = float(input("Enter pressure value?"))

# This function takes pressure values and the cordinates of the 2 points and returns a point on the line which has pressure value same as query pressure value 
def getcordinates(val1, val2, y, x):
    p1 =(((val1-pressure_value)/(val1-val2))*(x[0]-y[0]))+y[0]
    p2 =(((val1-pressure_value)/(val1-val2))*(x[1]-y[1]))+y[1]
    p3 =(((val1-pressure_value)/(val1-val2))*(x[2]-y[2]))+y[2]
    return (p1, p2, p3)

# Reading the vti file containing data
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName("Data/Isabel_2D.vti")
reader.Update()
data = reader.GetOutput()

# Extracting number of cells
numCells = data.GetNumberOfCells()
points = vtkPoints()
dataArray = vtkFloatArray()
dataArray.SetName('Pressure')

# Looping through cells in the grid
for i in range(numCells):
    
    cell = data.GetCell(i)
    
    # Storing the pid of the 4 corner points of the cells
    pid1 = cell.GetPointId(0)
    pid2 = cell.GetPointId(1)
    pid3 = cell.GetPointId(3)
    pid4 = cell.GetPointId(2)
    
    dataArr = data.GetPointData().GetArray('Pressure')
    
    # Storing the pressure values of 4 corner points of the cell
    val1 = dataArr.GetTuple1(pid1)
    val2 = dataArr.GetTuple1(pid2)
    val3 = dataArr.GetTuple1(pid3)
    val4 = dataArr.GetTuple1(pid4)
    
    # Storing the cordinates of the 4 corner points of the cell
    a = data.GetPoint(pid1)
    b = data.GetPoint(pid2)
    c = data.GetPoint(pid3)
    d = data.GetPoint(pid4)
    
    # These 16 conditions finds the 2 points to draw a line
    if (val1>pressure_value and val2>pressure_value and val3>pressure_value and val4>pressure_value):
        continue
    elif val1<pressure_value and val2<pressure_value and val3<pressure_value and val4<pressure_value:
        continue
    elif val1<pressure_value and val2<pressure_value and val3<pressure_value and val4>pressure_value:
        l = getcordinates(val4, val3, d, c)
        r = getcordinates(val4, val1, d, a)
    elif val1<pressure_value and val2<pressure_value and val3>pressure_value and val4<pressure_value:
        l = getcordinates(val3, val2, c, b)
        r = getcordinates(val3, val4, c, d)
    elif val1<pressure_value and val2<pressure_value and val3>pressure_value and val4>pressure_value:
        l = getcordinates(val4, val1, d, a)
        r = getcordinates(val3, val2, c, b)
    elif val1<pressure_value and val2>pressure_value and val3<pressure_value and val4<pressure_value:
        l = getcordinates(val2, val1, b, a)
        r = getcordinates(val2, val3, b, c)
    elif val1<pressure_value and val2>pressure_value and val3<pressure_value and val4>pressure_value:
        l = getcordinates(val2, val1, b, a)
        r = getcordinates(val2, val3, b, c)
    elif val1<pressure_value and val2>pressure_value and val3>pressure_value and val4<pressure_value:
        l = getcordinates(val2, val1, b, a)
        r = getcordinates(val3, val4, c, d)
    elif val1<pressure_value and val2>pressure_value and val3>pressure_value and val4>pressure_value:
        l = getcordinates(val2, val1, b, a)
        r = getcordinates(val4, val1, d, a)
    elif val1>pressure_value and val2<pressure_value and val3<pressure_value and val4<pressure_value:
        l = getcordinates(val1, val2, a, b)
        r = getcordinates(val1, val4, a, d)
    elif val1>pressure_value and val2<pressure_value and val3<pressure_value and val4>pressure_value:
        l = getcordinates(val1, val2, a, b)
        r = getcordinates(val4, val3, d, c)
    elif val1>pressure_value and val2<pressure_value and val3>pressure_value and val4<pressure_value:
        l = getcordinates(val1, val2, a, b)
        r = getcordinates(val3, val2, c, b)
    elif val1>pressure_value and val2<pressure_value and val3>pressure_value and val4>pressure_value:
        l = getcordinates(val1, val2, a, b)
        r = getcordinates(val3, val2, c, b)
    elif val1>pressure_value and val2>pressure_value and val3<pressure_value and val4<pressure_value:
        l = getcordinates(val2, val3, b, c)
        r = getcordinates(val1, val4, a, d)
    elif val1>pressure_value and val2>pressure_value and val3<pressure_value and val4>pressure_value:
        l = getcordinates(val2, val3, b, c)
        r = getcordinates(val4, val3, d, c)
    elif val1>pressure_value and val2>pressure_value and val3>pressure_value and val4<pressure_value:
        l = getcordinates(val3, val4, c, d)
        r = getcordinates(val1, val4, a, d)
      
    # Inserting the 2 points in points array  
    points.InsertNextPoint(l)
    points.InsertNextPoint(r)
    dataArray.InsertNextTuple1(pressure_value)
    dataArray.InsertNextTuple1(pressure_value)

polyLine = vtkPolyLine()
cells = vtkCellArray()

# creating the polyline by connecting the line between points discovered in each cell
for i in range(0, points.GetNumberOfPoints(), 2):
    polyLine.GetPointIds().SetNumberOfIds(2)    
    polyLine.GetPointIds().SetId(0, i)
    polyLine.GetPointIds().SetId(1, i+1)
    cells.InsertNextCell(polyLine)

# Creaeing polydata to hold points, cells, and pressure data and generating the vtp file.
pdata = vtkPolyData()
pdata.SetPoints(points)
pdata.SetLines(cells)
pdata.GetPointData().AddArray(dataArray)
writer = vtkXMLPolyDataWriter()
writer.SetInputData(pdata)
writer.SetFileName('contour1.vtp')
writer.Write()