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

from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

from qtile_extras import widget

import os
import subprocess

@hook.subscribe.startup_once
def autostart():
	home = os.path.expanduser ('~/.config/qtile/autostart.sh')
	subprocess.Popen([home])

mod = "mod4"
terminal = "kitty"

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
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


colors = [
            ["#ffffff60", "#ffffff60"], #0 White transparent color for BAR
            ["#ffffff", "#ffffff"],     #1 BAR COLOR
            ["#00000050", "#00000050"], #2 Highlight_block color
            ["#01a1f5", "#01a1f5"],     #3 BAR BORDER BLUE AZURE
            ["#030706", "#030706"],     #4 BG COLORS 3
            ["#9faec3", "#9faec3"],     #5 Foreground Light
            ["#dc793e", "#dc793e"],     #6 Orange
            ["#bc444b", "#bc444b"],     #7 pink to orange gradient?
            ]

############GROUP󰖲󰖯S##########

groups = []
group_names = ["G1", "G2", "G3", "G4"]
keynames = [i for i in "1234"]
#group_labels = ["󱂬", "󱂬","󱂬","󱂬"]
#group_labels = ["", "", "", ""]
group_labels = ["󰗘", "󰗘", "󰗘", "󰗘"]
for g in range(len(group_names)):
    groups.append(
            Group(
                name=group_names[g],
                label=group_labels[g],
                )
            )

# mod + i, moves screen to groups [i]
# mod + shift + i, moves screen with active tab groups [i]

for keyname, group in zip(keynames, groups):
    keys.extend([
        Key([mod], keyname, lazy.group[group.name].toscreen()),
        Key([mod, "shift"], keyname, lazy.window.togroup(group.name)),

        ])

layout_theme = {
        "border_width": 1,
        "margin": 10,
        "border_focus ": colors[3],
        "border_normal": colors[3],

        }


layouts = [
    #layout.Columns(),
    #layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(**layout_theme, border_focus=colors[3]),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="MesloGM Nerd Font Mono",
    fontsize = 16,
    padding_y= 2,
    foreground=colors[1],
)
extension_defaults = widget_defaults.copy()

def no_text(text):
    return ""

screens = [
    Screen(
        bottom=bar.Bar(
            [   
               widget.Sep(foreground="#00000000", padding = 2),
               
               widget.TextBox(
                    '󰜬', 
                    fontsize = 24,
                    padding_y = 8,
                    highlight_method = 'block',
                   ),
               #widget.LaunchBar(
                                #progs = [
                                #        ('󰜬', 'rofi -show drun'),
                                #        ],
                                #font = 'Arial',
                                #fontsize = 20,
                                #text_only = True,
                                #highlight_method = 'block',
                                #highlight_color = [2],
                                #this_current_screen_border = colors[2],
                                #this_screen_border = colors[2],
                                #background = colors[2],
                                #padding = 6, 
                                #),
               #widget.QuickExit(
                                #default_text='󰕮',
                                #default_text='󰜬',
                                #default_text='󰙀',
                                #countdown_format ="{}",
                                #countdown_font_size = 4,
                                #font = "Arial",
                                #fontsize = 19,
                                #padding = 10,
                                # ), 
                widget.Sep(foreground="#00000000", padding = 4),
                
                #widget.CurrentLayout(),
                widget.GroupBox(

                    font = "MesloLGS Nerd Font Mono", 
                    fontsize = 24, 
                    borderwidth = 1,
                    active = colors[1], 
                    inactive = colors[2], 
                    margin_x = 2, 
                    padding_x = 8,
                    padding_y = 2,
                    highlight_method = 'block',
                    block_highlight_text_color = colors[1],
                    #highlight_color = [0],
                    this_current_screen_border = colors[2],
                    this_screen_border = colors[2],
                    center_aligned = True, 
                    disable_drag = True,
                    urgent_alert_method = 'block', 
                    urgent_border=colors[2],
                    urgent_text = colors[1],

                    ),

                widget.Sep(foreground="#00000000", padding = 8),

                #widget.WindowName(
                    #max_chars = 15,
                    #background="#00000050"
                    #),
                widget.TaskList(
                    #background="#000000",
                    #foreground=colors[2],
                    #font="MesloLGS Nerd Font Mono",
                    #highlight_method = 'block',
                    #border = colors[2],
                    borderwidth = 0,
                    icon_size=18,
                    padding_x = 5,
                    #margin_x = 20,
                    parse_text=no_text,
                    txt_minimized="",
                    txt_maximized="",
                    
                    txt_floating='',
                    #theme_mode = 'preferred',
                    #theme_path = '/home/al2/.icons/Win11',
                    ),
                widget.Spacer(),
                
                widget.Prompt(font = "Arial", fontsize = 12, prompt = "{prompt} : "),
                widget.TextBox("󰍹", fontsize = 16),
                widget.Net(
                        font = "Arial",
                        fontsize = 11,
                        format='{down:.0f}{down_suffix} ↓↑ {up:.0f}{up_suffix}'),
                widget.Volume(step = 1, pading= 10, fontsize = 20, scroll = True, scroll_fixed_width=True, emoji=True, emoji_list = ['󰝟', "󰕿", "󰖀", "󱄠"] ),

                widget.TextBox(" ", fontsize = 16, padding = 2 ),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Systray(),
                widget.Clock(
                    font = "Arial",
                    fontsize = 11,
                    padding = 8,
                    format="%I:%M %p" "\n" "%d/%m%y"
                    ),
                widget.Sep(foreground=colors[0], linewidth = 8, size_percent = 100),
            ],
            30, border_width=0, border_color=colors[3], background=colors[0],                
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
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
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
        border_width = 1, border_focus = "#01a1f5", border_normal = "#01a1f5",
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

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

