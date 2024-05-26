document.getElementById('createMissionForm').addEventListener('submit', function (event) {
    event.preventDefault(); // Evitar o envio padrão do formulário

    // Capturar os dados do formulário
    const nome_missao = document.getElementById('nome_da_missao').value;
    const data_lancamento = document.getElementById('data da lancamento').value;
    const destino = document.getElementById('destino').value;
    const estado_missao = document.getElementById('status_da_missao').value;
    const duracao_missao = document.getElementById('duracao').value;
    const custo_missao = parseFloat(document.getElementById('mission_cost').value);
    const tripulacao = document.getElementById('tripulacao').value;
    const cargautil = document.getElementById('cargautil').value;

    // Criar objeto de missão
    const missao = {
        nome_missao: nome_missao,
        data_lancamento: data_lancamento,
        destino: destino,
        estado_missao: estado_missao,
        tripulacao: tripulacao,
        carga_util: cargautil,
        duracao_missao: duracao_missao,
        custo_missao: custo_missao,
        status_missao: estado_missao
    };

    // Chamar a função para cadastrar a missão
    cadastrarMissao(missao)
        .then(data => {
            console.log('Missão cadastrada com sucesso:', data);
            document.getElementById('errorMessage').style.display = 'none'; // Esconder mensagem de erro, se visível
            document.getElementById('successMessage').innerText = 'Missão cadastrada com sucesso!';
            document.getElementById('successMessage').style.display = 'block'; // Mostrar mensagem de sucesso

            // Limpar os campos do formulário após o sucesso
            document.getElementById('nome_da_missao').value = '';
            document.getElementById('data da lancamento').value = '';
            document.getElementById('destino').value = '';
            document.getElementById('status_da_missao').value = '';
            document.getElementById('duracao').value = '';
            document.getElementById('mission_cost').value = '';
            document.getElementById('tripulacao').value = '';
            document.getElementById('cargautil').value = '';
        })
        .catch(error => {
            console.error('Erro ao cadastrar missão:', error);
            document.getElementById('errorMessage').innerText = error.message;
            document.getElementById('errorMessage').style.display = 'block'; // Mostrar mensagem de erro
        });
});

// Função para cadastrar uma nova missão
async function cadastrarMissao(missao) {
    try {
        const response = await fetch('http://127.0.0.1:2961/criar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(missao)
        });

        if (response.ok) {
            const data = await response.json();
            console.log('Missão cadastrada com sucesso:', data);
            return data;
        } else {
            const errorData = await response.json();
            console.error('Erro ao cadastrar missão:', errorData);
            throw new Error(errorData.message || 'Erro desconhecido ao cadastrar missão');
        }
    } catch (error) {
        console.error('Erro ao fazer solicitação:', error);
        throw error;
    }
}

// Função para limpar tabela

function limparDados() {
    const tableBody = document.getElementById('missions_table').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = ''; // Limpar o conteúdo atual da tabela
}

// Função para vizualizar todas as missões

function visualizarTodasMissoes() {
    fetch('http://127.0.0.1:2961/visualizar')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('missions_table').getElementsByTagName('tbody')[0];
            tableBody.innerHTML = ''; // Limpar o conteúdo atual da tabela
            data.forEach(missao => {

                // Criar uma nova linha na tabela para cada missão
                const row = tableBody.insertRow();

                // Preencher as células da linha com os dados da missão
                const cellid = row.insertCell(0);
                const cellNomeMissao = row.insertCell(1);
                const cellDataLancamento = row.insertCell(2);
                const cellDestino = row.insertCell(3);
                const cellEstadoMissao = row.insertCell(4);
                const cellDuracaoMissao = row.insertCell(5);

                // Função para formatar a data no estilo brasileiro (dia/mês/ano)
                function formatarDataBrasileira(data) {
                    const dataObj = new Date(data);
                    const dia = String(dataObj.getDate()).padStart(2, '0');
                    const mes = String(dataObj.getMonth() + 1).padStart(2, '0'); // Mês começa do zero
                    const ano = dataObj.getFullYear();
                    return `${dia}/${mes}/${ano}`;
                }

                // Preencher as células com os dados da missão
                cellid.innerText = missao.id;
                cellNomeMissao.innerText = missao.nome_missao;
                cellDataLancamento.innerText = formatarDataBrasileira(missao.data_lancamento);
                cellDestino.innerText = missao.destino;
                cellEstadoMissao.innerText = missao.estado_missao;
                cellDuracaoMissao.innerText = missao.duracao_missao;

            });
        })
        .catch(error => {
            console.error('Erro ao buscar dados das missões:', error);
            // Lidar com erros, se houver algum
        });
}


// Função para deletar a missão
function deletarMissao(event) {
    event.preventDefault(); // Evitar o envio padrão do formulário

    // Capturar o ID da missão a ser excluída
    const idMissao = document.getElementById('delete_mission_id').value;

    // Chamar a função para deletar a missão
    deletarMissaoAPI(idMissao);
}

// Função para enviar a solicitação de exclusão para a API
async function deletarMissaoAPI(idMissao) {
    try {
        const response = await fetch('http://127.0.0.1:2961/deletar', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: idMissao })
        });

        if (response.ok) {
            console.log('Missão excluída com sucesso');
            // Faça aqui o que for necessário após excluir a missão, como recarregar a lista de missões
            visualizarTodasMissoes(); // Recarrega a lista de missões após excluir uma
        } else {
            console.error('Erro ao excluir missão:', response.statusText);
            // Tratar o erro de acordo com sua lógica de usuário
        }
    } catch (error) {
        console.error('Erro ao excluir missão:', error);
        // Tratar o erro de acordo com sua lógica de usuário
    }
}




// Função para editar

async function buscarMissao() {
    const idMissao = document.getElementById('mission_id').value;

    try {
        const response = await fetch(`http://127.0.0.1:2961/visualizar/${idMissao}`);
        if (response.ok) {
            const missao = await response.json();
            preencherFormulario(missao);
        } else {
            exibirMensagem('Erro ao buscar missão: ' + response.statusText);
        }
    } catch (error) {
        exibirMensagem('Erro ao buscar missão: ' + error.message);
    }
}

function preencherFormulario(missao) {
    document.getElementById('nome_da_missaoed').value = missao.nome_missao;
    document.getElementById('data_da_lancamentoed').value = missao.data_lancamento;
    document.getElementById('destinoed').value = missao.destino;
    document.getElementById('status_da_missaoed').value = missao.estado_missao;
    document.getElementById('duracaoed').value = missao.duracao_missao;
    document.getElementById('mission_costed').value = missao.custo_missao;
    document.getElementById('tripulacaoed').value = missao.tripulacao;
    document.getElementById('cargautiled').value = missao.carga_util;
}

async function atualizarMissao(event) {
    event.preventDefault();

    const missao = {
        id: document.getElementById('mission_id').value,
        nome_missao: document.getElementById('nome_da_missaoed').value,
        data_lancamento: document.getElementById('data_da_lancamentoed').value,
        destino: document.getElementById('destinoed').value,
        estado_missao: document.getElementById('status_da_missaoed').value,
        duracao_missao: document.getElementById('duracaoed').value,
        custo_missao: parseFloat(document.getElementById('mission_costed').value),
        tripulacao: document.getElementById('tripulacaoed').value,
        carga_util: document.getElementById('cargautiled').value
    };

    try {
        const response = await fetch('http://127.0.0.1:2961/atualizar', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(missao)
        });

        if (response.ok) {
            const data = await response.json();
            exibirMensagem('Missão atualizada com sucesso');
            limparFormulario();
        } else {
            const errorData = await response.json();
            exibirMensagem('Erro ao atualizar missão: ' + (errorData.message || 'Erro desconhecido'));
        }
    } catch (error) {
        exibirMensagem('Erro ao fazer solicitação: ' + error.message);
    }
}

function exibirMensagem(mensagem) {
    const mensagemElement = document.createElement('p');
    mensagemElement.textContent = mensagem;
    mensagemElement.classList.add('mensagem-sucesso');
    const containerMensagem = document.getElementById('mensagem');
    containerMensagem.innerHTML = '';
    containerMensagem.appendChild(mensagemElement);
    setTimeout(() => {
        containerMensagem.removeChild(mensagemElement);
    }, 3000);
}

function limparFormulario() {
    document.getElementById('missionFormAt2').reset();
}


function limparFormulario() {
    document.getElementById('missionForm').reset();
}











