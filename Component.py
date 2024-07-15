from Constants import VHDL_LIBRARIES, VHDL_LIBRARY_DECLARATION
import os

class Component:
    """
    Base class for all VHDL components
    """

    @property
    def name(self)->str:
        return ''
    
    def getEntity(self)->str:
        """
        Return entity delaration of  component or raise error is not implemented
        """
        raise NotImplementedError()
    
    def getComponent(self)->str:
        """
        Return component definition of VHDL Component or raise error is not implemented
        """
        raise NotImplementedError()
    
    def getInstance(self)->str:
        """
        Return component instance as a string or raise error is not implemented
        """
        raise NotImplementedError()
    
    def toVHDL(self)->str:
        """
        return complete VHDL defintion of component
        """
        return NotImplementedError()
    
    def writeToFle(self)->None:
        """
        write VHDL component to file
        """
        if not os.path.exists('vhdl_files'):
            os.makedirs('vhdl_files')
        with open(f'vhdl_files/{self.name}.vhd', 'w') as file:
            file.write(self.toVHDL())

        print("Done writing")