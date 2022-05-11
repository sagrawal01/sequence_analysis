Coding Script
------------

In this script, we are writing functions to analyze input DNA/RNA sequences  and verify their mass, generate shipping labels, and validate the sequence.

In the command line, navigate to the folder where you have downloaded code and docker image file (synthego_assignment) and run `$docker build -t USERNAME/PROJECT:VERSION . ` (i.e. `$docker build -t sagrawal01/sequence_analysis:v1 . `) to build the docker image from the file. 

Run `$docker images` to check that your image was built. Once you see it, run `$docker run -it -v (current working directory):/app USERNAME/PROJECT:VERSION /bin/bash` in command line. This will run the container. Then navigate to analyze_sequence.py and do the following:

1. To determine (base-sugar units and linkages), run the following example command on terminal inside the docker container:
   `python3 analyze_sequence.py RUN_BASE_SUGAR_UNITS -Uro-Uro-Gro-Ums-Um`
    
2. To calcuate the molecular mass of the sequence, run the following example command on terminal inside the docker container:
   `python3 analyze_sequence.py RUN_CALCULATE_MASS -Uro-Uro-Gro-Ums-Um '{"-Ur":1.0011, "-Gr": 1, "-Um":2, "o":1, "s": 3}'`
    
3. To generate shipping label from sequence, run the following example command on terminal inside the docker container:
    `python3 analyze_sequence.py RUN_GENERATE_SHIPPING_LABEL -Gdo-Gdo-Ado-Ado-Tdo-Gro-Gro-Cro-Uro-Uro-Uro-Ur`

4. To validate sequence data, run the following example command on terminal inside the docker container:
    `python3 analyze_sequence.py RUN_SEQUENCE_CHECKER -Gro-Gro-Gro-Ums-Am`
