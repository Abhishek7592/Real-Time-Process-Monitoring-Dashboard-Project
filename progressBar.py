 def updateProgress_bar(self, bar, value):
        bar["value"] = value
        if value > 90:
            bar["style"] = "Red.Horizontal.TProgressbar"
        elif value > 60:
            bar["style"] = "Yellow.Horizontal.TProgressbar"
        else:
            bar["style"] = "Green.Horizontal.TProgressbar"

        bar.update_idletasks()
