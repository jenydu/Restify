/*
 * controller.js
 *
 * Write all your code here.
 */

///////////////////////////////////* part 1 *///////////////////////////////////

// Function to validate the username field
function validateUsername(username) {
  const regex = /^[a-zA-Z0-9_]{6,}$/;
  if (!regex.test(username)) {
    return 'Username is invalid';
  }
  return '';
}

// Function to validate the password field
function validatePassword(password) {
  const regex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*])(?=.{8,})/
  if (!regex.test(password)) {
    return 'Password is invalid';
  }
  return '';
}

// Function to validate the repeat password field
function validateRepeatPassword(password, repeatPassword) {
  if (password !== repeatPassword) {
    return "Passwords don't match";
  }
  return '';
}

// Function to validate the email field
function validateEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const domain = email.split('@')[1];
  if (!regex.test(email) || email.includes('..') || domain.includes('_')) {
    return 'Email is invalid';
  }
  return '';
}

// Function to validate the phone field
function validatePhone(phone) {
  const regex = /^\d{3}-\d{3}-\d{4}$/;
  if (!regex.test(phone)) {
    return 'Phone is invalid';
  }
  return '';
}

// Function to validate a form field
function validateField(field, validator) {
  const value = field.val().trim();
  const error = validator(value);
  if (error) {
    field.addClass('is-invalid');
    field.next().text(error);
  } else {
    field.removeClass('is-invalid');
    field.next().text('');
  }
}

// Attach an event listener to each input field to validate it on change
$(document).ready(function() {
  const usernameField = $('#username');
  const passwordField = $('#password1');
  const repeatPasswordField = $('#password2');
  const emailField = $('#email');
  const phoneField = $('#phone');
  const registerButton = $('#register');
  const notification = $('#notification');

  usernameField.on('change', function() {
    validateField(usernameField, validateUsername);
  });

  passwordField.on('change', function() {
    validateField(passwordField, validatePassword);
    validateField(repeatPasswordField, function() {
      return validateRepeatPassword(passwordField.val(), repeatPasswordField.val());
    });
  });

  repeatPasswordField.on('change', function() {
    validateField(repeatPasswordField, function() {
      return validateRepeatPassword(passwordField.val(), repeatPasswordField.val());
    });
  });

  emailField.on('change', function() {
    validateField(emailField, validateEmail);
  });

  phoneField.on('change', function() {
    validateField(phoneField, validatePhone);
  });
  //////////
  registerButton.on('click', function() {

    validateField(usernameField, validateUsername);
    validateField(passwordField, validatePassword);
    validateField(repeatPasswordField, function() {
      return validateRepeatPassword(passwordField.val(), repeatPasswordField.val());
    });
    validateField(emailField, validateEmail);
    validateField(phoneField, validatePhone);

    if (usernameField.hasClass('is-invalid') ||
      passwordField.hasClass('is-invalid') ||
      repeatPasswordField.hasClass('is-invalid') ||
      emailField.hasClass('is-invalid') ||
      phoneField.hasClass('is-invalid')) {
      notification.html("<p>At least one field is invalid. Please correct it before proceeding</p>");
    } else {
      notification.html('<p>User added</p>');
      $('#username_notification').html('<p>Username has already been taken</p>');
    }
  });

  ///////////////////////////////////* part 2 *///////////////////////////////////
  $('#add_update_item').on('click', function() {
    // Get the input values
    const name = $('#name').val().trim();
    const price = ($('#price').val());
    const quantity = ($('#quantity').val());

    // Validate the input
    if (name === '' || isNaN(price) || isNaN(quantity) || price < 0 || quantity < 0) {
      $('#item_notification').html('<p>Name, price, or quantity is invalid</p>');
    }

    let itemExists = false;
    $('#cart-items tr').each(function() {
      let rowname = $(this).find('td:first').text();
      if (name == rowname) {
        itemExists = true;
        const price = parseFloat($('#price').val());
        const quantity = parseInt($('#quantity').val());

        let curr_total = $(this).find('td:nth-child(4)').text();
        curr_total = parseFloat(curr_total.substring(1));

        $(this).find('td:nth-child(2)').text('$' + price.toFixed(2));
        $(this).find('td:nth-child(3)').text(quantity);
        $(this).find('td:nth-child(4)').text('$' + (price * quantity).toFixed(2));

        const subtotal = parseFloat($('#subtotal').text());

        // Add the new item total to the existing subtotal
        const newSubtotal = subtotal - curr_total + (price * quantity);
        const newTaxes = newSubtotal * 0.13;
        const newGrandTotal = newSubtotal + newTaxes;
        // Update the subtotal display with the new subtotal value
        $('#subtotal').text(newSubtotal.toFixed(2));
        $('#taxes').text(newTaxes.toFixed(2));
        $('#grand_total').text(newGrandTotal.toFixed(2));
        return false;
      }
    });

    if (!itemExists) {
      newitem = new Item(name, parseFloat(price), parseInt(quantity));

      let rowId = newitem.name.replace(/\s+/g, '_');
      let row = $('<tr>').attr('id', rowId);
      let nameCol = $('<td>').text(newitem.name);
      let priceCol = $('<td>').text('$' + newitem.price.toFixed(2));
      let quantityCol = $('<td>').text(newitem.quantity);
      let totalCol = $('<td>').text('$' + newitem.total.toFixed(2));

      let decreaseBtn = $('<button>').addClass('btn decrease').text('-');
      let increaseBtn = $('<button>').addClass('btn increase').text('+');
      let deleteBtn = $('<button>').addClass('btn delete').text('delete');
      let btnCol1 = $('<td>').append(decreaseBtn);
      let btnCol2 = $('<td>').append(increaseBtn);
      let btnCol3 = $('<td>').append(deleteBtn);

      row.append(nameCol, priceCol, quantityCol, totalCol, btnCol1, btnCol2, btnCol3);
      $('#cart-items').append(row);

      // calculate new total
      const subtotal = parseFloat($('#subtotal').text());
      // Add the new item total to the existing subtotal
      const newSubtotal = subtotal + newitem.total;
      const newTaxes = newSubtotal * 0.13;
      const newGrandTotal = newSubtotal + newTaxes;
      // Update the subtotal display with the new subtotal value
      $('#subtotal').text(newSubtotal.toFixed(2));
      $('#taxes').text(newTaxes.toFixed(2));
      $('#grand_total').text(newGrandTotal.toFixed(2));
    }
    $('#name').val('');
    $('#price').val('');
    $('#quantity').val('');
    $('#item_notification').text('');
  });

  $("#cart-items").on('click', '.btn.delete', function() {
    $(this).closest('tr').remove();
  });

  $("#cart-items").on('click', '.btn.decrease', function() {
    let curr_price = $(this).closest('tr').find('td:nth-child(2)').text();
    let curr_total = $(this).closest('tr').find('td:nth-child(4)').text();
    let quantity = $(this).closest('tr').find('td:nth-child(3)').text();

    newquantity = parseInt(quantity) - 1;
    if (newquantity >= 0) {
      new_total = parseFloat(curr_total.substring(1)) - parseFloat(curr_price.substring(1));
      $(this).closest('tr').find('td:nth-child(3)').text(newquantity);
      $(this).closest('tr').find('td:nth-child(4)').text('$' + new_total.toFixed(2));

      const subtotal = parseFloat($('#subtotal').text());
      const newSubtotal = subtotal - parseFloat(curr_price.substring(1));
      const newTaxes = newSubtotal * 0.13;
      const newGrandTotal = newSubtotal + newTaxes;
      $('#subtotal').text(newSubtotal.toFixed(2));
      $('#taxes').text(newTaxes.toFixed(2));
      $('#grand_total').text(newGrandTotal.toFixed(2));
    }
  });

  $("#cart-items").on('click', '.btn.increase', function() {
    let curr_price = $(this).closest('tr').find('td:nth-child(2)').text();
    let curr_total = $(this).closest('tr').find('td:nth-child(4)').text();
    let quantity = $(this).closest('tr').find('td:nth-child(3)').text();

    newquantity = parseInt(quantity) + 1;
    if (newquantity >= 0) {
      new_total = parseFloat(curr_total.substring(1)) + parseFloat(curr_price.substring(1));
      $(this).closest('tr').find('td:nth-child(3)').text(newquantity);
      $(this).closest('tr').find('td:nth-child(4)').text('$' + new_total.toFixed(2));

      const subtotal = parseFloat($('#subtotal').text());
      const newSubtotal = subtotal + parseFloat(curr_price.substring(1));
      const newTaxes = newSubtotal * 0.13;
      const newGrandTotal = newSubtotal + newTaxes;
      $('#subtotal').text(newSubtotal.toFixed(2));
      $('#taxes').text(newTaxes.toFixed(2));
      $('#grand_total').text(newGrandTotal.toFixed(2));
    }
  });

  ///////////////////////////////////* part 3 *///////////////////////////////////
  // detect when the user has scrolled to the bottom of the page

  $.ajax({
    url: '/text/data?paragraph=' + 1,
    method: "GET",
    dataType: "json",
    success: function(data) {
      if (!data.next) {
        var end = $('<b>').text('You have reached the end');
        data_div.append(end);
      }
      var paragraphs = data.data;
      var data_div = $('#data');

      for (var i = 0; i < paragraphs.length; i++) {
        var paragraph = paragraphs[i];
        var paragraph_div = $('<div>').attr('id', 'paragraph_' + (i + 1));
        var content_p = $('<p>').text(paragraph.content);
        var p_num = $('<b>').text('(Paragraph: ' + (i + 1) + ')');
        var like_button = $('<button>').addClass('btn like').text('Likes: ' + paragraph.likes);
        paragraph_div.append(content_p, p_num, like_button);
        data_div.append(paragraph_div);
      }
    },
    error: function(jqXHR, textStatus, errorThrown) {
      console.log(jqXHR);
      console.log(textStatus);
      console.log(errorThrown);
    }
  });

  par_count = 6
  $(window).scroll(function() {
    if ($(window).scrollTop() + $(window).height() > $(document).height() - .90 * $(document).height() & par_count % 5 == 1) {
      $.ajax({
        url: '/text/data?paragraph=' + (par_count),
        method: "GET",
        dataType: "json",
        success: function(data) {
          var paragraphs = data.data;
          var data_div = $('#data');
          for (var i = 0; i < paragraphs.length; i++) {
            var paragraph = paragraphs[i];
            var paragraph_div = $('<div>').attr('id', 'paragraph_' + par_count);
            var content_p = $('<p>').text(paragraph.content);
            var p_num = $('<b>').text('(Paragraph: ' + par_count + ')');
            var like_button = $('<button>').addClass('btn like').text('Likes: ' + paragraph.likes);
            paragraph_div.append(content_p, p_num, like_button);
            data_div.append(paragraph_div);
            par_count++;
          }
          if (!data.next) {
            var end = $('<b>').text('You have reached the end');
            data_div.append(end);
          }
        },
        error: function(jqXHR, textStatus, errorThrown) {
          console.log(jqXHR);
          console.log(textStatus);
          console.log(errorThrown);
        }
      });
    }
  });

  $("#data").on('click', '.btn.like', function() {
    var like_button = $(this);
    var paragraph_id = parseInt($(this).parent().attr('id').split('_')[1]);
    $.ajax({
      url: '/text/like',
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({
        'paragraph': paragraph_id
      }),
      dataType: 'json',
      success: function(data) {
        like_button.text('Likes: ' + data.data.likes);
      }
    });
  });
});