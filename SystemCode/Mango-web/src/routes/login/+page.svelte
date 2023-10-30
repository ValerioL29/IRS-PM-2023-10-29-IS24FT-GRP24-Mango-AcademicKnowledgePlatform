<script>
	import { enhance } from "$app/forms";
	
    const background_url = "bg-2.jpg";
</script>

<div class="hero min-h-screen" style="background-image: url({background_url});">
	<div class="hero-overlay bg-base-100 bg-opacity-70"></div>
	<div class="hero-content flex-col lg:flex-row-reverse">
		<div class="text-center w-auto">
			<h1 class="text-8xl font-bold text-black">🥭 Login now!</h1>
			<h2 class="py-6 text-black">
				🫲 Mango is your best academic assistant 🫱 <br/>
			</h2>
			<a class="btn btn-secondary text-white" href="/sign">					  
				Sign Up Here!
				<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
					<path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
				</svg>
			</a>
		</div>
		<div class="card flex-shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
			<form class="card-body" method="POST" action="/login?/login" use:enhance>
				<div class="form-control p-2">
					<span class="text-lg pl-1 pb-2">Username / Email</span>
					<input name="email" type="text" class="input input-bordered" required />
				</div>
				<div class="form-control p-2">
					<span class="text-lg pl-1 pb-2">Password</span>
					<input name="password" type="password" class="input input-bordered" required />
				</div>
				<div class="form-control mt-6">
					<button class="btn btn-primary text-white">Login</button>
				</div>
			</form>
		</div>
	</div>
</div>
