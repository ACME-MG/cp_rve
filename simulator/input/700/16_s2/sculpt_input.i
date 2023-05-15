
    BEGIN SCULPT

        # Dimensions
        nelx = 16
        nely = 16
        nelz = 16

        # Fixed mesh improvement
        smooth = 2
        pillow_curves = true
        pillow_boundaries = true
        micro_shave = true
        scale = 2

        # Variable mesh improvement
        # defeature = 1
        opt_threshold = 0.7
        pillow_curve_layers = 3
        pillow_curve_thresh = 0.3
        
        # Solver
        laplacian_iters = 5
        max_opt_iters = 50
        
        # Output files
        input_spn = ./results/230501224212_16/rve.spn
        exodus_file = ./results/230501224212_16/mesh.e
        
    END SCULPT
    