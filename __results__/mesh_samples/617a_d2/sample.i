
BEGIN SCULPT
    
    # Dimensions
    nelx = 3
    nely = 83
    nelz = 137

    # Mesh Improvement
    smooth = 2
    defeature = 1
    remove_bad = 0.0

    # Remove cuts
    void_mat = 1
    
    # Solver
    laplacian_iters = 10
    max_opt_iters = 100
    # adapt_type = 5
    # adapt_levels = 1
    
    # Output
    input_spn = ./results/221208231607/sample.spn
    exodus_file = ./results/221208231607/sample

END SCULPT
