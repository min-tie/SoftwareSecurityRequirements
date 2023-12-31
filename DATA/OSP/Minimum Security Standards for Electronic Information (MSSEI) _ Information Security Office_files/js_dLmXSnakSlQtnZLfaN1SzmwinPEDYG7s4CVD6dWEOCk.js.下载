/**
 * @file
 * JS for Radix.
 */
(function ($, Drupal, window, document, undefined) {
  // Allow dropdown links to be clickable by showing dropdowns on hover/focus.
  Drupal.behaviors.radix_dropdown = {
    attach: function(context, setting) {
      var dropdown_disabled = false,
          deferred_timeout = null;

      // Prevent the dropdown from re-opening if a menu link was focused before
      // the window was re-focused.
      $(window).focus(function() {
        dropdown_disabled = true;
        setTimeout(function () {
          dropdown_disabled = false;
        }, 0);
      });

      $('.dropdown').once('radix-dropdown', function() {
        var dropdown = this;

        // Helper function to show the dropdown.
        function show() {
          if (!$(dropdown).hasClass('open') && !dropdown_disabled) {
            $('>[data-toggle="dropdown"]', dropdown).trigger('click.bs.dropdown');
          }
        }

        // Defer calling show() so that this happens after the click handler
        // below (for Android support).
        function deferredShow() {
          clearTimeout(deferred_timeout);
          deferred_timeout = setTimeout(function () {
            show();
          }, 0);
        }

        // Helper function to hide the dropdown.
        function hide() {
          if ($(dropdown).hasClass('open')) {
            $('>[data-toggle="dropdown"]', dropdown).trigger('click.bs.dropdown');
          }
        }

        // Show dropdown on hover and focus.
        $(this).on('mouseenter.radix.dropdown', function(e) {
          deferredShow();
        });
        $(this).on('mouseleave.radix.dropdown', function() {
          hide();
        });
        $(this).on('focusin.radix.dropdown', function() {
          deferredShow();
        });

        // Fix for Android: only allow clicking the link after the dropdown menu has
        // opened - the first click will just open the dropdown.
        $('>a', this).on('click.radix.dropdown', function(e) {
          if (!$(this).parent().hasClass('open')) {
            show();
            return false;
          }
        });

        $(this).on('keydown.radix.dropdown', function(e) {
          // Prevent up/down arrow from doing anything -- they conflict with
          // using focus to show the dropdown, and the default Bootstrap keydown
          // handler will trigger our click handler to visit the link.
          if (e.keyCode == 38 || e.keyCode == 40) {
            return false;
          }
          // Show/hide dropdown with spacebar.
          if (e.keyCode == 32) {
            $('>[data-toggle="dropdown"]', dropdown).trigger('click.bs.dropdown');
            return false;
          }
          // Hide the dropdown with the escape hey.
          if (e.keyCode == 27) {
            // Leave focus on the parent after it's hidden.
            $('>[data-toggle="dropdown"]', dropdown).focus();
            hide();
            return false;
          }
        });

        // Allow a.dropdown-toggle to be clickable.
        if ($(this).has('> a.dropdown-toggle')) {
          $(this).on('click.radix.dropdown', function(e) {
            var $target = $(e.target);
            if ($target.parent().get(0) == dropdown && $target.is('a.dropdown-toggle') && $target.attr('href')) {
              e.preventDefault();
              window.location.href = $target.attr('href');
            }
          });
        }
      });

      // Make submenus work.
      $('.dropdown-submenu').once('radix-dropdown', function() {
        var dropdown = this,
            toggle = $(dropdown).children('.dropdown-toggle'),
            menu = $(dropdown).children('.dropdown-menu');

        function show() {
          $(dropdown).addClass('open');
        }

        // Defer calling show() so that this happens after the click handler
        // below (for Android support).
        function deferredShow() {
          clearTimeout(deferred_timeout);
          deferred_timeout = setTimeout(function () {
            show();
          }, 0);
        }

        function hide() {
          $(dropdown).removeClass('open');
        }

        $(dropdown)
          .on('mouseenter.radix.dropdown', deferredShow)
          .on('mouseleave.radix.dropdown', hide)
          .on('focusin.radix.dropdown', deferredShow);

        // Fix for Android: only allow clicking the link after the dropdown menu has
        // opened - the first click will just open the dropdown.
        $('>a', this).on('click.radix.dropdown', function(e) {
          if (!$(this).parent().hasClass('open')) {
            show();
            return false;
          }
        });
      });

      // Hide dropdowns when focus is lost.
      $('body').once('radix-dropdown').on('focusout.radix.dropdown', function(e) {
        var parent = $(e.target).closest('li.radix-dropdown-processed.open').get(0);
        if (parent) {
          // Defer to after all handlers so we can see where focus landed.
          setTimeout(function () {
            // Don't do anything if no element is focused - that can only
            // happen with the mouse and this is meant to close the menu
            // when the keyboard is used to change focus.
            if (!document.activeElement || document.activeElement === document.body) {
              return;
            }
            // Hide the parent if it doesn't contain the now focused element
            // and is still open.
            if (!parent.contains(document.activeElement) && $(parent).hasClass('open')) {
              if ($(parent).hasClass('dropdown-submenu')) {
                $(parent).removeClass('open');
              }
              else {
                $(parent).trigger('click.bs.dropdown');
              }
            }
          }, 0);
        }
      });

    }
  };

  // Bootstrap tooltip.
  Drupal.behaviors.radix_tooltip = {
    attach: function(context, setting) {
      if ($.fn.tooltip) {
        $("[data-toggle='tooltip']").tooltip();
      }
    }
  };

  // Bootstrap popover.
  Drupal.behaviors.radix_popover = {
    attach: function(context, setting) {
      if ($.fn.popover) {
        $("[data-toggle='popover']").popover();
      }
    }
  };

  $(document).ready(function() {
    // Show first tab by default.
    // Ignore the "primary" tabs on the node edit page.
    if ($.fn.tab) {
      var tabs = $('.nav-tabs').not('.primary');
      tabs.children('li').first().find('a').tab('show');

      if (hash = window.location.hash) {
        $('.nav-tabs > li > a[href$="' + hash + '"]').tab('show');
      }
    }
  });
})(jQuery, Drupal, this, this.document);
;
/**
 * @file
 * Custom scripts for theme.
 */

(function ($) {
  function makeRoomForAdminMenu() {
    var menu_height = $('#admin-menu').height(),
        body_margin = parseInt($('body.admin-menu').css('margin-top'));

    if (menu_height !== body_margin) {
      $('body.admin-menu').attr('style', 'margin-top: ' + menu_height + 'px !important');
    }
  }

  function convertTd2Th(row) {
    $(row).children('td').replaceWith(function () {
      var attrs = {}, i;
      // Replace the 'td' with a 'th' that has all the same attrs.
      for (i = 0; i < this.attributes.length; i++) {
        attrs[this.attributes[i].nodeName] = this.attributes[i].nodeValue;
      }
      return $('<th></th>').html(this.innerHTML).attr(attrs);
    });
  }

  function normalizeTable(table) {
    // Look for row headers without scope="row" and add it!
    $(table).find('>tbody > tr').has('th').each(function () {
      if ($(this).children('td').length > 0) {
        // If we have some data cells, then we assume that any header cells
        // in the first column were meant to be row headers!
        $(this).children('th:first-child').attr('scope', 'row');
      }
    });

    // Convert a faux header into a real header if the markup is funky.
    // Check that the table has no thead and has more than one row.
    if ($(table).children('thead').length === 0 && $(table).children('tbody').children('tr').length > 1) {
      var faux_thead = $(table).find('>tbody:first-of-type > tr:first-child'),
          header_cells = $(faux_thead).children('td,th'),
          header_lengths = header_cells.map(function () { return this.textContent.length; }).get();

      if (faux_thead.has('th[scope="row"]').length) {
        // If we have a row header, then this is probably a data row and not a
        // header!
      }
      else if (Math.max.apply(null, header_lengths) > 40 && !faux_thead.has('th').length) {
        // A header row wouldn't have labels this long. And in any case, long
        // labels won't really work with the inline header styling we're using.
      }
      else if (faux_thead.find('img,table').length > 0) {
        // If there are certain tags in the header, then this seems like a data
        // row and we shouldn't mess with it.
      }
      else if (header_cells.length == 1 && parseInt(header_cells.eq(0).attr('colspan')) > 1) {
        // If the header is a single cell with a colspan of greater than one,
        // this was probably really meant to be a <caption> tag. However, we
        // don't full support <caption>s in OB, so for now just punting!
        // @todo: Convert these type of rows into captions!
      }
      else {
        // Huzzah! We think this is a header row, so let's make it one. :-)
        var thead = $('<thead></thead>').insertBefore($('>tbody:first-of-type', table)),
            next_faux_thead = null,
            row_count = 1;

        // Figure out how many rows we need to grab.
        header_cells.each(function () {
          var rowspan = parseInt($(this).attr('rowspan'));
          if (rowspan > 1 && rowspan > row_count) {
            row_count = rowspan;
          }
        });

        // Add them to the thead.
        do {
          next_faux_thead = faux_thead.next();
          faux_thead.remove();
          convertTd2Th(faux_thead);
          thead.append(faux_thead);
          faux_thead = next_faux_thead;
        }
        while (faux_thead.length && --row_count > 0);
      }
    }

    // The WYSIWYG can generate some empty tbody tags, remove 'em!
    $(table).children('tbody:empty').remove();

    // If the first cell in any data row is a row header, then assume the user
    // intended for all the cells in the same position to also be row headers.
    if ($(table).find('>tbody > tr > th:first-child[scope="row"]').length > 0) {
      var rowspan = 1;
      $(table).find('>tbody > tr > th:first-child, >tbody > tr > td:first-child').each(function () {
        var attrs = {}, i;

        // Skip subsequent rows for rowspan.
        if (rowspan > 1) {
          rowspan--;
          return;
        }
        rowspan = this.rowSpan;

        if ($(this).is('td')) {
          // Replace the 'td' with a 'th' that has all the same attrs (plus
          // scope="row").
          for (i = 0; i < this.attributes.length; i++) {
            attrs[this.attributes[i].nodeName] = this.attributes[i].nodeValue;
          }
          attrs['scope'] = 'row';
          $(this).replaceWith($('<th></th>').html(this.innerHTML).attr(attrs));
        }
        else {
          $(this).attr('scope', 'row');
        }
      });
    }
  }

  // Returns a two dimensional array of table cells.
  function getTableArray(table) {
    var rows = [];

    $(table).find('>tbody > tr').each(function (row) {
      $(this).children('td,th').each(function (col) {
        if (typeof rows[row] === 'undefined') {
          rows[row] = [];
        }
        rows[row][col] = this;
      });
    });

    return rows;
  }

  // Fills in table with hidden elements for rowspan and colspan.
  function fillTableSpans(table) {
    var col;

    function cloneNode(node) {
      var clone = node.cloneNode(true);
      $(clone).addClass('openberkeley-linearizable-table-hidden-cell');
      clone.removeAttribute('rowspan');
      clone.removeAttribute('colspan');
      return clone;
    }

    $(table).find('tr').each(function () {
      col = 0;
      $(this).children('td,th').each(function () {
        var colspan = $(this).attr('colspan'),
            rowspan = $(this).attr('rowspan'),
            curRow = this.parentNode,
            x, y;

        // Defaults.
        if (!colspan) {
          colspan = 1;
        }
        if (!rowspan) {
          rowspan = 1;
        }

        // Clone elements for colspan.
        if (colspan > 1) {
          for (y = 1; y < colspan; y++) {
            this.parentNode.insertBefore(cloneNode(this), this.nextElementSibling);
          }
        }

        // Clone elements for rowspan.
        if (rowspan > 1) {
          for (x = 1; x < rowspan; x++) {
            for (y = 0; y < colspan; y++) {
              if (curRow && curRow.nextElementSibling) {
                curRow.nextElementSibling.insertBefore(cloneNode(this), curRow.nextElementSibling.children[col + y]);
              }
            }
            curRow = curRow.nextElementSibling;
          }
        }

        // Store the original colspan and rowspan.
        if (colspan > 1) {
          this.setAttribute('data-original-colspan', colspan);
        }
        if (rowspan > 1) {
          this.setAttribute('data-original-rowspan', rowspan);
        }

        col += colspan;
      });
    });
  }

  function makeTableLinearizable(table) {
    fillTableSpans(table);

    var column_headers = $(table).find('>thead > tr:first-of-type > th'),
        column_labels = [],
        // At the moment, we only support row headers in the first cell.
        row_headers = $(table).find('>tbody > tr > th:first-child[scope="row"]'),
        rows = getTableArray(table);

    column_headers.each(function () {
      var content = this.innerText || this.textContent;

      // Clean up whitespace in content.
      content = content.replace(/nbsp;/g, ' ');
      content = content.replace(/^\n/m, '');
      content = content.replace(/\n$/m, '');
      content = content.replace(/\n/g, ', ');
      content = content.replace(/^\s+/m, '');
      content = content.replace(/\s+$/m, '');

      column_labels.push(content);
    });

    // Add the data-th="..." attribute.
    $.each(rows, function (row_index) {
      var cells = this;

      // Sanity check on this row.
      if (!$.isArray(cells) || cells.length !== column_headers.length) {
        return;
      }

      // Do the actual work.
      $.each(cells, function (col_index) {
        var header = column_labels[col_index];
        if (header) {
          $(this).attr('data-th', header);
        }
      });
    });

    // Mark as a linearizable table so the CSS magic will happen.
    $(table).addClass('openberkeley-linearizable-table');
  }

  // Toggles class marking linearized table, as linearized, and modifies the
  // rowspan/colspan to keep the table semantic when hiding/showing hidden
  // cells.
  function toggleTablesLinearized() {
    var linearized = $(window).width() < 768;
    $('table.openberkeley-linearizable-table').each(function () {
      if ($(this).hasClass('openberkeley-linearized-table') !== linearized) {
        if (linearized) {
          $('[data-original-colspan],[data-original-rowspan]', this).attr({
            rowspan: 1,
            colspan: 1,
          });
        }
        else {
          $('[data-original-colspan],[data-original-rowspan]', this).each(function () {
            if (this.hasAttribute('data-original-colspan')) {
              this.colSpan = this.getAttribute('data-original-colspan');
            }
            if (this.hasAttribute('data-original-rowspan')) {
              this.rowSpan = this.getAttribute('data-original-rowspan');
            }
          });
        }

        $(this).toggleClass('openberkeley-linearized-table', linearized);
      }
    });
  }

  Drupal.behaviors.openberkeley_theme_base = {
    attach: function (context, settings) {
      // Normalize settings to prevent errors. This can happen when this script
      // is loaded in an iframe, which didn't render the full page template.
      if (typeof settings.openberkeley_theme_base === 'undefined') {
        settings.openberkeley_theme_base = {};
      }

      // Make image maps responsive if we have the jQuery plugin for it.
      if (typeof $.fn.rwdImageMaps !== 'undefined') {
        var $img = $('img[usemap]', context);
        if ($img.length) {
          $img.once().rwdImageMaps();
        }
      }

      // Modify the markup for tables created in WYSIWYG:
      //
      //   1. Add some default Bootstrap classes
      //   2. Wrap in div.table-responsive so that super wide tables get
      //      horizontal scrollbars.
      //
      $('table', context)
        .not('.sticky-header')
        .filter(function () {
          return !$(this).closest('.table-responsive').length && !$(this).closest('.mceEditor').length;
        })
        .addClass('table-bordered')
        .addClass('table-striped')
        .wrap('<div class="table-responsive"></div>')
        .each(function () {
          $('tbody tr:nth-child(odd)', this).addClass('odd');
          $('tbody tr:nth-child(even)', this).addClass('even');
        });

      // Setup tables that were created in WYSIWYG to become linear if they
      // include the appropriate headers.
      if (!settings.openberkeley_theme_base.disable_linearizable_tables) {
        $('table:not(.openberkeley-linearizable-table)', context)
          .not('.sticky-header')
          .not('.openberkeley-not-responsive')
          .not('div.openberkeley-not-responsive table')
          .filter(function () {
            return !$(this).closest('.mceEditor').length;
          })
          .once('openberkeley-theme-base-linearizable-check')
          .each(function () {
            // Before attempting to add header attributes to all the table cells,
            // let's normalize the table markup.
            if (!settings.openberkeley_theme_base.disable_normalize_tables) {
              normalizeTable(this);
            }

            // Then make it linearizable!
            makeTableLinearizable(this);
          });
        toggleTablesLinearized();
      }

      // Unmark a table as linearizable if it has tabledrag enabled.
      if (typeof settings.tableDrag !== 'undefined') {
        $('table.openberkeley-linearizable-table', context)
          .filter(function () {
            return typeof settings.tableDrag[this.id] !== 'undefined';
          })
          .removeClass('openberkeley-linearizable-table');
      }

      // Apply a special class to linearizable tables that shouldn't become
      // lineor on print. We only want to linearize tables that wouldn't fit
      // within a 600px box.
      $('table.openberkeley-linearizable-table', context)
        .not('.sticky-header')
        .once('openberkeley-theme-base-print-check')
        .each(function () {
          var $this = $(this),
              parentDiv = $this.parent('.table-responsive');
          // We temporarily set the parentDiv to 600px and see if the table
          // overflows. If it does, then this needs to linearized on print, but
          // if not, then it doesn't need to be.
          parentDiv.css('width', '600px');
          if ($this.width() <= 600) {
            $this.addClass('openberkeley-dont-linearize-table-on-print');
          }
          parentDiv.css('width', '');
        });

      // Announce to screenreader users when menus close.
      if (typeof Drupal.announce !== 'undefined') {
        $('.dropdown', context).bind('hide.bs.dropdown', function () {
          var menu_name = $(this).find('> a:first-child').text();
          Drupal.announce(Drupal.t('@menu closed', {'@menu': menu_name}));
        });
      }

      // Add file icons for linked files.
      if (settings.openberkeley_theme_base.file_link_icons) {
        $($('#content', context).length > 0 ? '#content a' : 'a', context).not('.nav *').not('span.file *').not(':has(img)').not('.openberkeley-widgets-promo *').not('.openberkeley-widgets-hero *').once('openberkeley-theme-base-file-link-icons').each(function () {
          var href = this.href,
              exts = ['docx', 'doc', 'xlsx', 'xls', 'ppt', 'pptx', 'txt', 'rtf', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mpeg', 'mp4', 'avi', 'mov', 'mkv', 'mp3', 'wav', 'zip', 'gz', 'tar', 'pps', 'ppsx', 'odt', 'ods', 'odp'],
              extension_re = /\.([a-zA-Z0-9]{1,4})$/,
              match = href.match(extension_re),
              extension = match ? match[1] : null,
              external_text = $('span.ext', this),
              text;

          if (extension && exts.indexOf(extension) != -1) {
            // Mark the link with the right class.
            $(this).addClass('openberkeley-theme-link-ext-' + extension);

            // Put the invisible text after the link text, but before the
            // external link text.
            text = $('<span class="element-invisible"> (' + extension.toUpperCase() + ' file)</span>');
            if (external_text.length > 0) {
              text.insertBefore(external_text);
            }
            else {
              $(this).append(text);
            }

            // Put the icon before the link.
            $('<span class="openberkeley-theme-file-icon openberkeley-theme-file-icon-ext-' + extension + '">').insertBefore(this);
          }
        });
      }

      // Keyboard trap in Bootstrap modal.
      $('.modal', context).on('shown.bs.modal', function (e) {
        var $modal = $(e.target);
        $modal.once(function () {
          var tabbableElements = $modal.find(':tabbable');

          $(tabbableElements[0]).on('keydown.openucb', function (e) {
            if (e.which == 9 && e.shiftKey) {
              tabbableElements[tabbableElements.length - 1].focus();
              return false;
            }
          });
          $(tabbableElements[tabbableElements.length - 1]).on('keydown.openucb', function (e) {
            if (e.which == 9 && !e.shiftKey) {
              tabbableElements[0].focus();
              return false;
            }
          });
        });
      });

      // Some one-time page setup.
      $('body', context).once('openberkeley-theme-base', function () {
        // Make room for the admin menu immediately, and when window is resized.
        makeRoomForAdminMenu();
        $(window).resize(makeRoomForAdminMenu);

        // Toggle tables linearized on window resize.
        if (!settings.openberkeley_theme_base.disable_linearizable_tables) {
          $(window).resize(toggleTablesLinearized);
        }

        // Add aria-expanded=true/false on navbar toggle button.
        var navbar_toggle = $('.navbar-toggle[data-target="#navbar-collapse"]');
        $('#navbar-collapse')
          .on('hidden.bs.collapse', function () {
            navbar_toggle.attr({
              'aria-expanded': 'false',
              'aria-pressed': 'false'
            });
          })
          .on('show.bs.collapse', function () {
            navbar_toggle.attr({
              'aria-expanded': 'true',
              'aria-pressed': 'true'
            });
          });
        navbar_toggle.attr({
          'aria-expanded': 'false',
          'aria-pressed': 'false'
        });

        var visiblePageSelector = '#skip-link,#header,#main-wrapper,#footer,body > .region.region-page-bottom';
        $('.modal')
          // Move all dialogs to the bottom of the DOM.
          .appendTo($('body'))
          // Adjust focus and aria-hidden when modal is shown.
          .on('shown.bs.modal', function () {
            $(':tabbable:first', this).focus();
            $(visiblePageSelector).attr('aria-hidden', 'true');
          })
          // Restore focus and remove aria-hidden when modal goes away.
          .on('hidden.bs.modal', function () {
            var modal_id = this.id;
            $(visiblePageSelector).removeAttr('aria-hidden');
            $('[data-target="#' + modal_id + '"]:first').get(0).focus();
          });

        // Debugging code for tab order.
        /*
        $('body').focusin(function (e) {
          console.log('focus');
          console.log(e.target);
        });
        */

        // Defer until after all the other behaviors have run.
        setTimeout(function () {
          // Remove all the Radix dropdown behaviors from megamenus.
          $('.menu-fields-menu-link.radix-dropdown-processed', context)
            .off('.radix.dropdown')
            .on('keydown.openberkeley-base-theme.dropdown', function (e) {
              // Open/close the megamenu with the spacebar.
              if (e.keyCode == 32) {
                $('>[data-toggle="dropdown"]', this).trigger('click.bs.dropdown');
                return false;
              }
              // Hide the dropdown with the escape hey.
              else if (e.keyCode == 27 && $(this).hasClass('open')) {
                // Leave focus on the parent after it's hidden.
                $('>[data-toggle="dropdown"]', this).focus().trigger('click.bs.dropdown');
                return false;
              }
              // Up/down arrow keys should "tab" through the mega menu links.
              else if (e.keyCode == 40 || e.keyCode == 38) {
                var tabbable = $(':tabbable', this),
                    index = tabbable.index($(':focus'));

                // Open the megamenu if not open.
                if (!$(this).hasClass('open')) {
                  $('>[data-toggle="dropdown"]', this).trigger('click.bs.dropdown');
                }

                // Focus on the next or previous element.
                if (e.keyCode == 38) {
                  index--;
                }
                else {
                  index++;
                }
                if (index > 0 && index < tabbable.length) {
                  tabbable.eq(index).focus();
                }

                return false;
              }
            });
        }, 0);
      });
    }
  };

})(jQuery);
;
/**
 * @file
 * Light-weight backport of Drupal.announce() from Drupal 8.
 *
 * Use {@link Drupal.announce} to indicate to screen reader users that an
 * element on the page has changed state. For instance, if clicking a link
 * loads 10 more items into a list, one might announce the change like this.
 *
 * @example
 * $('#search-list')
 *   .on('itemInsert', function (event, data) {
 *     // Insert the new items.
 *     $(data.container.el).append(data.items.el);
 *     // Announce the change to the page contents.
 *     Drupal.announce(Drupal.t('@count items added to @container',
 *       {'@count': data.items.length, '@container': data.container.title}
 *     ));
 *   });
 */

(function (Drupal) {
 
  "use strict";

  // Only do this if Drupal.announce() isn't already defined!
  if (typeof Drupal.announce !== 'undefined') {
    return;
  }

  var liveElement;
  var announcements = [];
  var timeout = null;

  /**
   * Builds a div element with the aria-live attribute and add it to the DOM.
   *
   * @type {Drupal~behavior}
   */
  Drupal.behaviors.drupalAnnounce = {
    attach: function (context) {
      // Create only one aria-live element.
      if (!liveElement) {
        liveElement = document.createElement('div');
        liveElement.id = 'drupal-live-announce';
        liveElement.className = 'element-invisible';
        liveElement.setAttribute('aria-live', 'polite');
        liveElement.setAttribute('aria-busy', 'false');
        document.body.appendChild(liveElement);
      }
    }
  };

  /**
   * Concatenates announcements to a single string; appends to the live region.
   */
  function announce() {
    var text = [];
    var priority = 'polite';
    var announcement;

    // Create an array of announcement strings to be joined and appended to the
    // aria live region.
    var il = announcements.length;
    for (var i = 0; i < il; i++) {
      announcement = announcements.pop();
      text.unshift(announcement.text);
      // If any of the announcements has a priority of assertive then the group
      // of joined announcements will have this priority.
      if (announcement.priority === 'assertive') {
        priority = 'assertive';
      }
    }

    if (text.length) {
      // Clear the liveElement so that repeated strings will be read.
      liveElement.innerHTML = '';
      // Set the busy state to true until the node changes are complete.
      liveElement.setAttribute('aria-busy', 'true');
      // Set the priority to assertive, or default to polite.
      liveElement.setAttribute('aria-live', priority);
      // Print the text to the live region. Text should be run through
      // Drupal.t() before being passed to Drupal.announce().
      liveElement.innerHTML = text.join('\n');
      // The live text area is updated. Allow the AT to announce the text.
      liveElement.setAttribute('aria-busy', 'false');
    }

    timeout = null;
  }

  /**
   * Triggers audio UAs to read the supplied text.
   *
   * The aria-live region will only read the text that currently populates its
   * text node. Replacing text quickly in rapid calls to announce results in
   * only the text from the most recent call to {@link Drupal.announce} being
   * read. By wrapping the call to announce in a debounce function, we allow for
   * time for multiple calls to {@link Drupal.announce} to queue up their
   * messages. These messages are then joined and append to the aria-live region
   * as one text node.
   *
   * @param {string} text
   *   A string to be read by the UA.
   * @param {string} [priority='polite']
   *   A string to indicate the priority of the message. Can be either
   *   'polite' or 'assertive'.
   *
   * @return {function}
   *
   * @see http://www.w3.org/WAI/PF/aria-practices/#liveprops
   */
  Drupal.announce = function (text, priority) {
    // Save the text and priority into a closure variable. Multiple simultaneous
    // announcements will be concatenated and read in sequence.
    announcements.push({
      text: text,
      priority: priority
    });
    // Immediately invoke the function that debounce returns. 200 ms is right at
    // the cusp where humans notice a pause, so we will wait
    // at most this much time before the set of queued announcements is read.
    if (timeout) {
      clearTimeout(timeout);
    }
    timeout = setTimeout(announce, 200);
  };
})(Drupal);
;
/**
 * @file
 * Custom scripts for theme.
 */

(function ($) {
  // Note: we avoid jQuery inside iframes because it makes things a little
  // trickier. Working with the DOM directly is more verbose, but it's easier
  // to not mess up.

  // Utility function that takes a TinyMCE.Editor object and applies a function
  // to every element of a particular tag in the editor.
  function processTagInEditor(ed, tag_name, callback) {
    var iframe = ed.contentDocument,
        elements = iframe.getElementsByTagName(tag_name),
        i;

    for (i = 0; i < elements.length; i++) {
      callback(elements[i]);
    }
  }

  Drupal.behaviors.openberkeley_theme_brand = {
    attach: function (context, settings) {
      // Expand banner alert by default on desktop.
      $('.banner-alert', context).once('openberkeley-theme-brand', function () {
        if (window.matchMedia("(min-width: 992px)").matches) {
          if (sessionStorage.getItem('banner-alert') !== 'collapsed') {
            $('button[data-toggle="collapse"]').removeClass('collapsed');
            $('.collapse', this).collapse('show');
          }
        }

        $('.collapse', this)
          .on('hidden.bs.collapse', function () {
            sessionStorage.setItem('banner-alert', 'collapsed');
          })
          .on('shown.bs.collapse', function () {
            sessionStorage.removeItem('banner-alert');
          });
      });

      if (typeof tinyMCE !== 'undefined') {
        $('body').once('openberkeley-theme-brand-wysiwyg', function () {
          // Whenever a new tinymce editor is created ...
          tinyMCE.onAddEditor.add(function (mgr, ed) {
            // We add an event to fire after it's initialized, and add the
            // typekit fonts from the main page to the iframe.
            ed.onInit.add(function (ed) {
              var iframe = ed.contentDocument;

              $('style:contains("://use.typekit.net")').each(function () {
                var style = iframe.createElement('style');
                style.type = 'text/css';
                style.innerHTML = this.innerHTML;
                iframe.getElementsByTagName('head')[0].appendChild(style);
              });
            });

            // Assign some onclick handlers to toggle a class on images when clicked.
            ed.onLoadContent.add(function (ed, o) {
              $(ed.contentDocument).click(function (evt) {
                if (evt.target.tagName.toLowerCase() == 'img') {
                  $(evt.target).addClass('openberkeley-theme-brand-image-focused');
                }
                else {
                  processTagInEditor(ed, 'img', function (img) {
                    $(img).removeClass('openberkeley-theme-brand-image-focused');
                  });
                }
              });
            });
            // And remove any of these classes when getting the content back out.
            ed.onSaveContent.add(function (ed, o) {
              processTagInEditor(ed, 'img', function (img) {
                $(img).removeClass('openberkeley-theme-brand-image-focused');
              });
            });
          });
        });
      }

      // Hook into the IPE, and make sure the template has the 'container' class
      // is present when the IPE is open (so the IPE isn't full width).
      $('.panels-ipe-save, .panels-ipe-cancel, #panels-ipe-customize-page', context).once('openberkeley-theme-brand').click(function () {
        if ($('.mvpcreator-theme-full-width').length > 0) {
          if ($('.panels-ipe-editing').length > 0) {
            $('#main-content').removeClass('container');
          }
          else {
            $('#main-content').addClass('container');
          }
        }
      });
    }
  };
})(jQuery);
;
