#!/bin/bash

# tmux 세션 이름
SESSION="my_project"
WORKSPACE=/home/min/Workspace/Bootcamp_Project


# tmux 세션 시작
tmux new-session -d -s $SESSION

# 첫 번째 창에서 백엔드 서버 실행
tmux send-keys -t $SESSION 'cd $WORKSPACE/backend && ./start_backend.sh' C-m

# 두 번째 창 생성 및 프론트엔드 서버 실행
tmux new-window -t $SESSION:1
tmux send-keys -t $SESSION:1 'cd $WORKSPACE/frontend && ./start_frontend.sh' C-m

# 세 번째 창 생성 및 백엔드 로그 확인
tmux new-window -t $SESSION:2
tmux send-keys -t $SESSION:2 'tail -f $WORKSPACE/backend/backend.log' C-m

# 네 번째 창 생성 및 프론트엔드 로그 확인
tmux new-window -t $SESSION:3
tmux send-keys -t $SESSION:3 'tail -f $WORKSPACE/frontend/frontend.log' C-m

# tmux 세션에 연결
tmux attach-session -t $SESSION