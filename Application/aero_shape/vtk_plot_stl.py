


import vtk
import argparse
"""
Simple VTK example in Python to load an STL mesh and display with a manipulator.
Chris Hodapp, 2014-01-28, (c) 2014
@michael modified 2022-03-31
"""
class vtk_plot:
    """
    INPUT::

            para: --stl stl_file , command line input .stl file

            para: back_rgblist(r,g,b) clor to back ground

            para: actor_rgblist(r,g,b) clor to body color

    FUNCTION:

                give .stl file to display 3D animation , click mouse to get 3D view of body

    OUTPUT:

       animantion on screen

    """
    def __init__(
             self,
             stl_file,
             actor_rgblist=[32, 13, 0],
             back_rgblist=[0,0,0],
    ):
        """初始化 VTK 绘图对象，用于加载并显示 STL 三维模型。

        参数:
            stl_file (str): 要加载的 STL 文件路径。
            actor_rgblist (list): 模型颜色 RGB 列表，默认为深棕色。
            back_rgblist (list): 背景颜色 RGB 列表，默认为黑色。
        """


        self.stl_file = stl_file
        self.back_rgblist = back_rgblist
        self.actor_rgblist = actor_rgblist
    def render(self):
        """创建渲染窗口、加载 STL 模型并启动交互式三维显示。"""
        # Create a rendering window and renderer
        ren = vtk.vtkRenderer()
        renWin = vtk.vtkRenderWindow()
        renWin.AddRenderer(ren)
        # Create a RenderWindowInteractor to permit manipulating the camera
        iren = vtk.vtkRenderWindowInteractor()
        iren.SetRenderWindow(renWin)
        style = vtk.vtkInteractorStyleTrackballCamera()
        iren.SetInteractorStyle(style)
        #.stl file name
        polydata = self.loadStl()
        ren.AddActor(self.polyDataToActor(polydata))
        ren.SetBackground(int(self.back_rgblist[0]), int(self.back_rgblist[1]), int(self.back_rgblist[2]))
        print(self.back_rgblist)

        # enable user interface interactor
        iren.Initialize()
        renWin.Render()
        iren.Start()


    def loadStl(self):
        """Load the given STL file, and return a vtkPolyData object for it."""
        #fname  = self.stl_file
        reader = vtk.vtkSTLReader()
        reader.SetFileName(self.stl_file)
        reader.Update()
        polydata = reader.GetOutput()
        return polydata


    def polyDataToActor(self,polydata):
        """Wrap the provided vtkPolyData object in a mapper and an actor, returning
        the actor."""
        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            # mapper.SetInput(reader.GetOutput())
            mapper.SetInput(polydata)
        else:
            #vtkPolyData * pd = vtkPolyData::New();
            #someAlgorithm->SetInputData(pd);
            mapper.SetInputData(polydata)
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        # actor.GetProperty().SetRepresentationToWireframe()
        actor.GetProperty().SetColor(32, 13, 0)
        return actor

if __name__ == "__main__":
    #import BlacFramework.BlacToolbox.vtk_plot as vplt
    parser = argparse.ArgumentParser(
        description="Generate a blade from a configuration file"
    )
    #parser.add_argument("cfg", nargs="*")
    parser.add_argument("stl", nargs="*")
    args = parser.parse_args()
    c=0
    for i in args.stl:
        ibefore=i.endswith(".stl")
        stlFilename = i
        c += 1
    if c == 0:
        print('need .stl file in command line')
    stl_plt = vtk_plot(stlFilename)
    stl_plt.render()




