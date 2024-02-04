const remote_host = "http://localhost:5000/";

export const getter = (resource, process, setLoading, setErr) => {
	const target = remote_host + resource;
	console.log("Starting GET from ", target);
	fetch(target)
		.then((resp) => {
			if (!resp.ok) {
				throw new Error(`Status code from GETting ${target}: ${resp.status}`);
			}
			return resp.json();
		})
		.then((json) => {
			console.log("Response to GET from ", target, ": ", json);
			process(json);
		})
		.catch((err) => {
			console.error("Error GETting from ", target, ": ", err);
			setErr(err);
		})
		.finally(() => setLoading(false));
};

export const poster = (resource, data, callback) => {
	const target = remote_host + resource;
	console.log("Starting POST to ", target);
	fetch(target, {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify(data),
	})
		.then((resp) => {
			if (!resp.ok) {
				throw new Error(`Status code from POSTing ${target}: ${resp.status}`);
			}
			return resp.json();
		})
		.then((json) => {
			console.log("Response to POST to ", target, ": ", json);
			// Let the calling code handle what to do after a successful response
			if (callback) {
				callback(json);
			}
		})
		.catch((err) => {
			console.error("Error POSTing to ", target, ": ", err);
		});
};

export const deleter = (resource, data, getter) => {
	const target = remote_host + resource;
	console.log("Starting DELETE to ", target);
	fetch(target, {
		method: "DELETE",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify(data),
	})
		.then((resp) => {
			if (!resp.ok) {
				throw new Error(`Status code from DELETING ${target}: ${resp.status}`);
			}

			return;
		})
		.then(() => {
			console.log("Response to DELETE to ", target, ": ");
			// trigger re-poll
			getter();
		})
		.catch((err) => {
			console.log("Error POSTing to ", target, ": ", err);
		});
}