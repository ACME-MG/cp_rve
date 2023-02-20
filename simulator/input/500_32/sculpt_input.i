
    BEGIN SCULPT

        # Dimensions
        nelx = 32
        nely = 32
        nelz = 32

        # Mesh Improvement
        smooth = 2
        # defeature = 1
        pillow_curves = true
        pillow_boundaries = true
        pillow_curve_layers = 4
        pillow_curve_thresh = 0.3
        opt_threshold = 0.7
        micro_shave = true
        
        # Solver
        laplacian_iters = 5
        max_opt_iters = 50
        
        # Output files
        input_spn = ./results/230214223233_32/rve.spn
        exodus_file = ./results/230214223233_32/mesh.e
        
    END SCULPT
    