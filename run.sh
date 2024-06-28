#!/bin/bash

# Function to create a new tmux pane and run the command
run_in_new_pane() {
    tmux split-window -h -t greedy_session:$1 "python3 main.py -library ../release/lib/lib1.json -netlist ../release/netlists/design$2.v -cost_function ../release/cost_estimators/cost_estimator_$3 --outdir ../data/data${2}_${3}greedy --method greedy &> ../logs/design${2}_cost${3}greedy.log; echo 'Press Enter to close pane: design${2}_cost${3}...'; read"
    tmux select-layout -t greedy_session:$1 tiled
}

# Create logs directory if it doesn't exist
mkdir -p ../logs

# Create a new tmux session
tmux new-session -d -s greedy_session "bash"

# Iterate over design files and cost estimators
for design in {5..6}; do
    for cost_estimator in {2..8}; do
        # Check if the current pane count is a multiple of 4 to create a new window
        if (( ( (design - 5) * 8 + cost_estimator - 2) % 4 == 0 )); then
            tmux new-window -n "design${design}_cost${cost_estimator}" -t greedy_session "bash"
        fi

        # Calculate the target window index
        window_index=$(( ( (design - 5) * 8 + cost_estimator - 2) / 4 + 1))

        # Run the command in a new pane in the target window
        run_in_new_pane $window_index $design $cost_estimator
    done
done

# Attach to the tmux session
tmux attach -t greedy_session