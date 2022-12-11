#!/usr/bin/env ruby
#
# Check for changed recipes

Jekyll::Hooks.register :recipes, :post_init do |recipe|

    # commit_num = `git rev-list --count HEAD "#{ recipe.path }"`
    # print `echo "THING #{ commit_num } #{ recipe.path }"`

    # if commit_num.to_i > 1
    lastmod_timestamp = `git log -1 --pretty="%ad" --date=unix "#{ recipe.path }"`
    recipe.data['last_modified_timestamp'] = lastmod_timestamp.strip.to_i

    lastmod_date = `git log -1 --pretty="%ad" --date=iso-strict "#{ recipe.path }"`
    recipe.data['last_modified_date'] = lastmod_date.strip
    # end

  end
