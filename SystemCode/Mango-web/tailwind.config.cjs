/** @type {import('tailwindcss').Config}*/
const config = {
	content: [
		'./src/**/*.{html,js,svelte,ts}'
	],

	theme: {
		extend: {}
	},

	plugins: [require("daisyui")],
	daisyui: {
		themes: ["emerald", "night"],
	},
};

module.exports = config;
