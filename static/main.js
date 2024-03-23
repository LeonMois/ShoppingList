var counter = 1;
function extendRecipeFields(document) {
  document
    .querySelector(".ingredient_form")
    .appendChild(document.createElement("br"));
  var select_field = document.createElement("SELECT");
  select_field.setAttribute("type", "text");
  select_field.setAttribute("name", "recipe_ingredient_" + counter);
  select_field.setAttribute("form", "recipe_form");
  document.querySelector(".ingredient_form").appendChild(select_field);
  document
    .querySelector(".ingredient_form")
    .appendChild(document.createElement("br"));
  var select = document.getElementsByName("recipe_ingredient_" + counter);
  var options = document.getElementsByName("option");
  select.forEach((element) => {
    options.forEach((option) => {
      opt = document.createElement("option");
      opt.text = option.text;
      element.add(opt);
    });
  });
  input_field = document.createElement("INPUT");
  input_field.setAttribute("type", "text");
  input_field.setAttribute("name", "amount_" + counter);
  input_field.setAttribute("placeholder", "Amount");
  input_field.setAttribute("form", "recipe_form");
  document.querySelector(".ingredient_form").appendChild(input_field);
  document
    .querySelector(".ingredient_form")
    .appendChild(document.createElement("br"));
  input_field = document.createElement("INPUT");
  input_field.setAttribute("type", "text");
  input_field.setAttribute("name", "unit_" + counter);
  input_field.setAttribute("placeholder", "Unit");
  input_field.setAttribute("form", "recipe_form");
  document.querySelector(".ingredient_form").appendChild(input_field);
  document
    .querySelector(".ingredient_form")
    .appendChild(document.createElement("br"));

  counter++;
}
