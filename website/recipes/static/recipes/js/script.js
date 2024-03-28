document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('add-row').addEventListener('click', function() {
        var tableBody = document.getElementById('ingredients_table').getElementsByTagName('tbody')[0];
        var newRow = tableBody.insertRow();
        newRow.innerHTML = `
            <td><input type="text" name="ingredient_name[]" class="ingredient-name"></td>
            <td><input type="text" name="ingredient_quantity[]" class="ingredient-quantity"></td>
            <td><input type="text" name="ingredient_unit[]" class="ingredient-unit"></td>
            <td><button type="button" class="remove-row">Remove</button></td>
        `;
    });

    document.getElementById('ingredients_table').addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-row')) {
            var row = e.target.parentNode.parentNode;
            row.parentNode.removeChild(row);
        }
    });
});
