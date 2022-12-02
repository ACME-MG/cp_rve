
    BEGIN SCULPT
        cell_size = 18.75
        nelx = 8
        nely = 8
        nelz = 8

        pillow = 3
        smooth = 2
        
        laplacian_iters = 10
        max_opt_iters = 100
        adapt_type = 5
        adapt_levels = 3

        defeature = 1
        micro_shave = true
        remove_bad = 0.0
        
        input_spn = ./results/rve.spn
        exodus_file = ./results/sculpt
    END SCULPT
    