root
{
	"defaultfont" "fonts/DroidSansMono.ttf"
	window
	{
		"title"		"Elements"
		"position"	"10 10"
		"size"		"250 500"
		"bgcolor"	"54 44 40 255"
		button
		{
			"text"		"2-Body (5 gold)"
			"position"	"14 48"
			"size"		"222 31"
			"bgcolor"	"127 77 56 255"
			"onclick"	"buypart"
			"part"		"2body"
		}
		button
		{
			"text"		"4-Body (10 gold)"
			"position"	"14 95"
			"size"		"222 31"
			"bgcolor"	"127 77 56 255"
			"onclick"	"buypart"
			"part"		"4body"
		}
		button
		{
			"text"		"Cannon (10 gold)"
			"position"	"14 142"
			"size"		"222 31"
			"bgcolor"	"127 77 56 255"
			"onclick"	"buypart"
			"part"		"cannon"
		}
	}
	window
	{
		"title"		"Resources"
		"position"	"10 526"
		"size"		"250 150"
		"bgcolor"	"54 44 40 255"
		label
		{
			"id"		"label_gold"
			"text"		"Gold: 0"
			"position"	"10 40"
		}
		label
		{
			"id"		"label_parts"
			"text"		"Parts: 0/100"
			"position"	"10 64"
		}
	}
	window
	{
		"title"		""
		"position"	"920 10"
		"size"		"350 75"
		"bgcolor"	"54 44 40 255"
		image
		{
			"path"		"textures/gui/wave.png"
			"position"	"10 10"
			"visible"	"false"
		}
		label
		{
			"id"		"label_wave"
			"text"		"Wave 1"
			"position"	"16 16"
			"font"		"fonts/DroidSerif-Bold.ttf"
			"font_size"	"36"
		}
	}
}