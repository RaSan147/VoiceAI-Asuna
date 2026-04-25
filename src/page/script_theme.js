/**
 * Optional UI preferences (density, reduced glass). Reads/writes localStorage.
 * Exposes window.AsunaUiTheme (class) and window.asunaUiTheme (singleton).
 */
class AsunaUiTheme {
	static STORAGE_KEY = "asuna_ui_theme_v1";

	/**
	 * @param {{ density?: "comfortable"|"compact", reducedGlass?: boolean }} [options]
	 */
	constructor(options) {
		this.options = Object.assign(
			{ density: "comfortable", reducedGlass: false },
			options || {}
		);
	}

	init() {
		const el = document.documentElement;
		let saved = null;
		try {
			saved = JSON.parse(localStorage.getItem(AsunaUiTheme.STORAGE_KEY));
		} catch (_) {}

		if (saved && typeof saved === "object") {
			if (saved.density === "compact" || saved.density === "comfortable") {
				this.options.density = saved.density;
			}
			if (saved.reducedGlass) this.options.reducedGlass = true;
		}

		el.dataset.uiDensity = this.options.density;

		if (this.options.reducedGlass) {
			el.dataset.reducedGlass = "1";
		} else if (
			window.matchMedia &&
			window.matchMedia("(prefers-reduced-transparency: reduce)").matches
		) {
			el.dataset.reducedGlass = "1";
		} else {
			el.removeAttribute("data-reduced-glass");
		}
	}

	/**
	 * @param {"comfortable"|"compact"} density
	 */
	setDensity(density) {
		if (density !== "comfortable" && density !== "compact") return;
		this.options.density = density;
		document.documentElement.dataset.uiDensity = density;
		this.persist();
	}

	/**
	 * @param {boolean} on
	 */
	setReducedGlass(on) {
		this.options.reducedGlass = !!on;
		const el = document.documentElement;
		if (this.options.reducedGlass) el.dataset.reducedGlass = "1";
		else el.removeAttribute("data-reduced-glass");
		this.persist();
	}

	persist() {
		try {
			localStorage.setItem(
				AsunaUiTheme.STORAGE_KEY,
				JSON.stringify({
					density: this.options.density,
					reducedGlass: this.options.reducedGlass,
				})
			);
		} catch (_) {}
	}
}

window.AsunaUiTheme = AsunaUiTheme;
window.asunaUiTheme = new AsunaUiTheme();
window.asunaUiTheme.init();
