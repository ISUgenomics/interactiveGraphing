# A quick guide for the InteractiveGraphing: Synteny

# The structure of code library

- `p` are `parameter` definition files, e.g., 
    - *p_generic.py* stores contant options, such as available built-in colors (they will never change)
    - *p_variables.py* stores custom options/tooltips, specific for this implementation (new can be added; once added they become constant)
   
- `f` are `function` definition files, e.g.,
    - *f_io.py* stores functions for managing and processing inputs and outputs
    - *f_widgets.py* stores functions for dynamic generation of various dash components (buttons, dropdowns, etc.)
    
- `l` are `layout` components files, e.g.,
    - *l_uploads* stores ready-made dash components for Input Upload section in the Options menu 
    - *l_analysis* stores ready-made dash components for pre-visualization analytical steps; Options menu