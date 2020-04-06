
# Tmux

```
tmux split-window -v
tmux split-window -h
tmux display-panes
tmux select-pane -t 3
tmux split-window 'man tmux'
```

```
$ cat source.tmux

#  +---------+---------+
#  |    0    |    1    |
#  +---------+---------+
#  |    2    |    3    |
#  +---------+---------+
#  |    4    |    5    |
#  +---------+---------+
#  |    6    |    7    |
#  +---------+---------+

new-window -n 2nd
split-window -v 'while true; do echo pane 4 ; sleep 1 ; done'
split-window -v 'while true; do echo pane 6 ; sleep 1 ; done'
select-pane -U
select-pane -U
split-window -v 'while true; do echo pane 2 ; sleep 1 ; done'
select-pane -t 0
split-window -h 'while true; do echo pane 1 ; sleep 1 ; done'
select-pane -D
split-window -h 'while true; do echo pane 3 ; sleep 1 ; done'
select-pane -D
split-window -h 'while true; do echo pane 5 ; sleep 1 ; done'
select-pane -D
split-window -h 'while true; do echo pane 7 ; sleep 1 ; done'
select-pane -t 0
split-window -v 'while true; do echo pane 0 ; sleep 1 ; done'

$ tmux source-file source.tmux
```
