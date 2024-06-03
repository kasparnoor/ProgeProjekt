<script lang="ts">
	import Saos from 'saos';
	import { onMount, tick } from 'svelte';
	import { Jumper } from 'svelte-loading-spinners';
	import axios from 'axios';
	// @ts-ignore
	import { saveAs } from 'file-saver';
	// @ts-ignore
	import { Plyr } from 'svelte-plyr';
	let player: { play: () => any; pause: () => any };
	let loading = false;
	let text: String;
	let textarea: HTMLTextAreaElement;
	export let videoId = 'wmG-Ip9foEk';
	let statusMessage;
	function logEvent(event: any) {
		console.log(event);
	}
	onMount(async () => {
		await tick();
		textarea.focus();

		// Add blur event listener to keep textarea focused
		textarea.addEventListener('blur', () => {
			textarea.focus();
		});
	});

	let is_enter_down = false;

	function on_key_down(event: KeyboardEvent) {
		// `keydown` event is fired while the physical key is held down.
		// In the switch-case we're updating our boolean flags whenever the
		// desired bound keys are pressed.
		switch (event.key) {
			case 'Enter':
				event.preventDefault();
				is_enter_down = true;
				loading = true;
				try {
					async function fetchVideo() {
						const response = await axios.post(
							'http://0.0.0.0:5001/post',
							{ text },
							{
								responseType: 'blob' // Ensure the response is in Blob format
							}
						);

						if (response.status === 200) {
							const blob = new Blob([response.data], { type: 'video/mp4' });
							saveAs(blob, 'received_video.mp4');
							statusMessage = 'Video saved as received_video.mp4';
						} else {
							statusMessage = `Failed to retrieve video. Status code: ${response.status}`;
						}
					}
				} catch (error) {
					// @ts-ignore
					statusMessage = `Error: ${error.message}`;
				}
				setTimeout(function () {
					loading = false;
				}, 1000);

				break;
		}
	}
</script>

<div class="h-[40vh] flex flex-col justify-center items-center bg-slate-900">
	<div class="text-center">
		<Saos animation={'text-focus-in 1s cubic-bezier(0.550, 0.085, 0.680, 0.530) both'}>
			<h1
				class="delay-100 font-black mb-6 text-5xl bg-gradient-to-r from-yellow-200 via-pink-300 to-purple-400 inline-block text-transparent bg-clip-text"
			>
				Tekstist video
			</h1>
		</Saos>
		<Saos animation={'text-focus-in 1s cubic-bezier(0.550, 0.085, 0.680, 0.530) both'}>
			<h3
				class="delay-100 font-black text-xl text-white inline-block text-transparent bg-clip-text"
			>
				Kirjelda millist videot soovid ja vajuta Enter.
			</h3>
		</Saos>
	</div>
</div>

<div class="custom-shape-divider-top-1715342076">
	<svg
		data-name="Layer 1"
		xmlns="http://www.w3.org/2000/svg"
		viewBox="0 0 1200 120"
		preserveAspectRatio="none"
	>
		<path
			d="M321.39,56.44c58-10.79,114.16-30.13,172-41.86,82.39-16.72,168.19-17.73,250.45-.39C823.78,31,906.67,72,985.66,92.83c70.05,18.48,146.53,26.09,214.34,3V0H0V27.35A600.21,600.21,0,0,0,321.39,56.44Z"
			class="shape-fill"
		></path>
	</svg>
</div>

<div class="h-[50vh] overflow-hidden flex items-center justify-center">
	{#if !is_enter_down}
		<textarea
			id="message"
			bind:value={text}
			bind:this={textarea}
			rows="4"
			class="focus:border-transparent block p-10 w-[100%] text-8xl outline-none focus:ring-0 text-gray-900 rounded-3xl m-4 h-full border-transparent"
			placeholder=""
		></textarea>
	{:else if loading}
		<Jumper size="120" color="#10172A" unit="px" duration="3s" />
	{:else}
		<h1 class="text-3xl">Video alla laadimine algas...</h1>
	{/if}
</div>

<svelte:window on:keydown={on_key_down} />

<style>
	.custom-shape-divider-top-1715342076 {
		position: relative;
		top: 0;
		left: 0;
		width: 100%;
		overflow: hidden;
		line-height: 0;
	}
	.custom-shape-divider-top-1715342076 svg {
		position: relative;
		display: block;
		width: calc(100% + 1.3px);
		height: 54px;
	}

	.custom-shape-divider-top-1715342076 .shape-fill {
		fill: #0f172a;
	}
	@-webkit-keyframes -global-tracking-in-expand {
		0% {
			letter-spacing: -0.5em;
			opacity: 0;
		}
		40% {
			opacity: 0.6;
		}
		100% {
			opacity: 1;
		}
	}
	@keyframes -global-tracking-in-expand {
		0% {
			letter-spacing: -0.5em;
			opacity: 0;
		}
		40% {
			opacity: 0.6;
		}
		100% {
			opacity: 1;
		}
	}

	@-webkit-keyframes -global-text-focus-in {
		0% {
			-webkit-filter: blur(12px);
			filter: blur(12px);
			opacity: 0;
		}
		100% {
			-webkit-filter: blur(0px);
			filter: blur(0px);
			opacity: 1;
		}
	}
	@keyframes -global-text-focus-in {
		0% {
			-webkit-filter: blur(12px);
			filter: blur(12px);
			opacity: 0;
		}
		100% {
			-webkit-filter: blur(0px);
			filter: blur(0px);
			opacity: 1;
		}
	}
</style>
