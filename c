{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1 class="mb-4">Apadrinhamento</h1>
    
    <div class="row g-4">
        {% for crianca in criancas %}
            <div class="col-md-4 col-sm-6">
                <div class="card h-100">
                    <div class="card-body text-center">
                        <div class="placeholder-image mb-3" style="width: 150px; height: 150px; background-color: #f0f0f0; margin: 0 auto;"></div>
                        <h5 class="card-title">{{ crianca.nome|slice:":1" }}, {{ crianca.idade }}</h5>
                    </div>
                </div>
            </div>
        {% endfor %}
    </div>
</div>

<style>
    .placeholder-image {
        border-radius: 4px;
    }
    .card {
        transition: transform 0.2s;
        cursor: pointer;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
</style>
{% endblock %}