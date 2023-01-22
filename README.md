# Screen Space Ambient Occlusion

## How to run

In order to run the project you need to have `path_to_project/SSAO/src` set as your working directory.

The very next thing is to simply run:

```shell
python ssao.py   
```


## Steering

You can move the camera throughout the scene using standard `WSAD` key bindings.
The pitch and yaw are controlled by mouse movements.

Additionally:

- `q` to roll to the right
- `e` to roll to the left,
- `space` to move up,
- `c` to move down,
- `,` to decrement SSAO samples count by 1,
- `.` to increment SSAO samples count by 1.
