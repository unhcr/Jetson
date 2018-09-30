Themify Icons SCSS
==================

This is a SCSS version of the Themify Icons which includes mixins to create themify icons on the fly. I am basing the SCSS off of the SCSS verion of font-awesome. You can find themify icons here: [http://themify.me/themify-icons](http://themify.me/themify-icons)

##Install
1. Download and put the themify-icons folder inside of your SASS folder.
2. Include themify in your main sass file  

	```
	@import 'themify-icons/themify-icons';

	```
3. Use as you wish

## About
This is currently in development, if you wish to help, please comment, fork, create issues, w/e you need.


## Usage
There are a few available variables you may use, below are some usages.

### Basic
This is the most basic usage. By default your icon will be displayed as a :before of your selected div. By default, your icon will be given  a font size of 18px, a margin right or left of 10px and a color of inherit.

```
.mydiv { @include icon($apple);  }
```

### Display after
This will display the icon as a :after on your selected div

```
.mydiv { @include iconafter($apple); }
```

### Variables
There are 3 variables currently set up for the icon: font-size, color, and margin. Below are their different uses:

#### All of them together (icon, margin, font-size, color)

```
.mydiv { @include icon($apple, 20px, 20px, $green); }
```

#### Just font size
```
.mydiv { @include icon($apple, $fs:20px); }
```
#### Just margin
```
.mydiv { @include icon($apple, $m:10px); }
```
#### Just color
```
.mydiv { @include icon($apple, $c:$purple); }
```
#### Removing defaults

```
.mydiv { @include icon($apple, null, null, $blue)
```

#### Available variables are
$fs for font-size

$m for margin

$c for color