
    BEGIN SCULPT
        nelx = 64
        nely = 64
        nelz = 64

        pillow = 3
        smooth = 2
        
        laplacian_iters = 10
        max_opt_iters = 100
        adapt_type = 5
        adapt_levels = 3

        defeature = 1
        micro_shave = true
        remove_bad = 0.0
        
        input_spn = ./results/221218163352_64/rve.spn
        exodus_file = ./results/221218163352_64/mesh.e
    END SCULPT
    