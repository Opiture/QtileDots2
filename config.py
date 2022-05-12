# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os, subprocess
from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = guess_terminal()

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.spawn("thunar"),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "d", lazy.spawn("rofi -show drun"), desc="Spawn a command using a prompt widget"),
    # RESIZE UP, DOWN, LEFT, RIGHT
    Key(
        [mod, "control"],
        "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
    ),
    Key(
        [mod, "control"],
        "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
    ),
    Key(
        [mod, "control"],
        "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
    ),
    Key(
        [mod, "control"],
        "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
    ),
    Key(
        [mod, "control"],
        "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
    ),
    Key(
        [mod, "control"],
        "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
    ),
    Key(
        [mod, "control"],
        "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
    ),
    Key(
        [mod, "control"],
        "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
    ),
]

groups = []

group_names = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
]

group_labels = [
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]

group_layouts = [
    "bsp",
    "bsp",
    "bsp",
    "bsp",
    "bsp",
    "bsp",
    "bsp",
    "bsp",
    "bsp",
    "bsp",
]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        )
    )

for i in groups:
    keys.extend(
        [
            # CHANGE WORKSPACES
            Key([mod], i.name, lazy.group[i.name].toscreen()),
            Key([mod], "Tab", lazy.screen.next_group()),
            Key([mod, "shift"], "Tab", lazy.screen.prev_group()),
            Key(["mod1"], "Tab", lazy.screen.next_group()),
            Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),
            # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
            # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name),
                lazy.group[i.name].toscreen(),
            ),
        ]
    )


layout_options = {"margin": 5, "border_width": 0}

def init_colors():
    return [
        ["#2e3440", "#2e3440"],  # color 0
        ["#3b4252", "#3b4252"],  # color 1
        ["#434c5e", "#434c5e"],  # color 2
        ["#4c566a", "#4c566a"],  # color 3
        ["#d8dee9", "#d8dee9"],  # color 4
        ["#e5e9f0", "#e5e9f0"],  # color 5
        ["#eceff4", "#eceff4"],  # color 6
        ["#88c0d0", "#88c0d0"],  # color 7
        ["#81a1c1", "#81a1c1"],  # color 8
        ["#5e81ac", "#5e81ac"],
    ]

colors = init_colors() 

layouts = [layout.Bsp(fair=False, **layout_options)]

widget_defaults = dict(
    font="Source Code Pro",
    fontsize=12,
    padding=3,
    background=colors[1]
)
extension_defaults = widget_defaults.copy()

def open_calcurse():
    qtile.cmd_spawn("alacritty -e calcurse")


def open_btm():
    qtile.cmd_spawn("alacritty -e btm")

def open_yay():
    qtile.cmd_spawn("alacritty -e yay -Syu")

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
            font="FontAwesome",
            fontsize=16,
            margin_y=3,
            margin_x=5,
            padding_y=0,
            padding_x=0,
            borderwidth=0,
            disable_drag=True,
            active=colors[9],
            inactive=colors[5],
            rounded=False,
            highlight_method="text",
            this_current_screen_border=colors[8],
            foreground=colors[2],
            background=colors[1],
        ),
        widget.WindowName(
            font="Source Code Pro",
            fontsize=16,
            foreground=colors[5],
            background=colors[1],
        ),
        widget.TextBox(
            font="FontAwesome",
            text="",
            foreground=colors[5],
            fontsize=16,
            mouse_callbacks={"Button1": open_yay},
        ),
        widget.CheckUpdates(
            display_format='{updates}',
            no_update_string='No updates',
            font="Source Code Pro",
            fontsize=16,
            mouse_callbacks={"Button1": open_yay},
        ),
        widget.Sep(linewidth=1, padding=10, foreground=colors[5], background=colors[1]),
        widget.TextBox(
            font="FontAwesome",
            text="",
            foreground=colors[5],
            fontsize=16,
            mouse_callbacks={"Button1": open_btm},
        ),
        widget.CPU(
            font="Source Code Pro",
            format="{load_percent}%",
            fontsize=16,
            foreground=colors[5],
            mouse_callbacks={"Button1": open_btm},
        ),
                widget.Sep(linewidth=1, padding=10, foreground=colors[5], background=colors[1]),
        widget.TextBox(
            font="FontAwesome",
            text="",
            foreground=colors[5],
            background=colors[1],
            padding=0,
            fontsize=16,
            mouse_callbacks={"Button1": open_btm},
        ),
        widget.Memory(
            font="Source Code Pro",
            format="{MemUsed: .0f}{mm}",
            update_interval=1,
            fontsize=16,
            foreground=colors[5],
            background=colors[1],
            mouse_callbacks={"Button1": open_btm},
        ),
        widget.Sep(linewidth=1, padding=10, foreground=colors[5], background=colors[1]),
        widget.Systray(
            background=colors[1],
            foreground=colors[5],
            icon_size=20,
            padding=0,
            margin=5,),
        widget.Sep(linewidth=1, padding=10, foreground=colors[5], background=colors[1]),
        widget.TextBox(
            font="FontAwesome",
            text=" ",
            foreground=colors[5],
            background=colors[1],
            padding=0,
            fontsize=16,
        ),
        widget.Battery(
            format="{percent:2.0%} {hour:d}:{min:02d}",
            font="Source Code Pro",
            foreground=colors[5],
            fontsize=16,
        ),
        widget.Sep(linewidth=1, padding=10, foreground=colors[5], background=colors[1]),
        widget.TextBox(
            font="FontAwesome",
            text="",
            foreground=colors[5],
            background=colors[1],
            padding=0,
            fontsize=16,
            mouse_callbacks={"Button1": open_calcurse},
        ),
        widget.Clock(
            font="Source Code Pro",
            foreground=colors[5],
            background=colors[1],
            fontsize=16,
            format="%d-%m-%Y %H:%M",
            mouse_callbacks={"Button1": open_calcurse},
        ),
        
                
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
            margin=[10, 10, 5, 10]
        ),
        bottom=bar.Gap(5),
        left=bar.Gap(5),
        right=bar.Gap(5),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]



dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

@hook.subscribe.startup_once
def start_once():
    home=os.path.expanduser('~')
    subprocess.call([home + "/.config/qtile/autostart.sh"])


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
