document.getElementById('new-transaction-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const sender = document.getElementById('sender').value;
    const recipient = document.getElementById('recipient').value;
    const amount = document.getElementById('amount').value;

    const response = await fetch('http://localhost:5000/transactions/new', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({ sender, recipient, amount }),
    });

    const data = await response.json();

    if (response.status === 201) {
        alert(data.message);
    } else {
        alert('Error: ' + data.error);
    }
});

document.getElementById('mine-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const miner = document.getElementById('miner').value;

    const response = await fetch('http://localhost:5000/mine', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({ miner }),
    });

    const data = await response.json();

    if (response.status === 200) {
        alert(data.message);
    } else {
        alert('Error: ' + data.error);
    }
});

document.getElementById('get-balances').addEventListener('click', async () => {
    const response = await fetch('http://localhost:5000/balances');
    const data = await response.json();

    if (response.status === 200) {
        let balancesMessage = "Balances of all customers:\n";
        for (const customerName in data.balances) {
            balancesMessage += `${customerName}: ${data.balances[customerName]}\n`;
        }
        alert(balancesMessage);
    } else {
        alert("Error: Unable to fetch customer balances.");
    }
});


async function getChain() {
    const response = await fetch('http://localhost:5000/chain');
    const data = await response.json();
    console.log(data)

    const chainContainer = document.getElementById('chain-container');
    chainContainer.innerHTML = '';

    data.chain.forEach((block) => {
        const blockElement = document.createElement('pre');
        blockElement.innerText = JSON.stringify(block, null, 2);
        chainContainer.appendChild(blockElement);
    });
}

document.getElementById('refresh-chain').addEventListener('click', getChain);

getChain();
