
    BEGIN SCULPT

        # Dimensions
        nelx = 32
        nely = 32
        nelz = 32

        # Fixed mesh improvement
        smooth = 2
        pillow_curves = true
        pillow_boundaries = true
        # defeature = 1
        micro_shave = true

        # Variable mesh improvement
        opt_threshold = 0.7
        pillow_curve_layers = 3
        pillow_curve_thresh = 0.3
        
        # Solver
        laplacian_iters = 5
        max_opt_iters = 50
        
        # Output files
        input_spn = ./results/230221003609_32/rve.spn
        exodus_file = ./results/230221003609_32/mesh.e
        
    END SCULPT
    