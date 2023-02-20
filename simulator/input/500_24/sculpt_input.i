
    BEGIN SCULPT

        # Dimensions
        nelx = 24
        nely = 24
        nelz = 24

        # Fixed mesh improvement
        smooth = 2
        pillow_curves = true
        pillow_boundaries = true
        # defeature = 1
        micro_shave = true

        # Variable mesh improvement
        pillow_curve_layers = 4
        pillow_curve_thresh = 0.3
        opt_threshold = 0.6
        
        # Solver
        laplacian_iters = 5
        max_opt_iters = 50
        
        # Output files
        input_spn = ./results/230220225824_24/rve.spn
        exodus_file = ./results/230220225824_24/mesh.e
        
    END SCULPT
    